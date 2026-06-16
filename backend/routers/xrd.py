"""
XRD 数据处理路由
提供 XRD 数据处理与可视化数据接口
"""

from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from pathlib import Path
from typing import List
import io
import numpy as np
import torch

from xrd_processor import xrd_process

router = APIRouter(tags=["XRD"])


class XRDDataPoint(BaseModel):
    angle: float  # 2-theta 角度 (度)
    intensity: float  # 强度


class ProcessRequest(BaseModel):
    data: List[XRDDataPoint]  # XRD 原始数据 [{angle, intensity}, ...]
    min_angle: float = 5.0
    max_angle: float = 90.0
    step: float = 0.01
    sigma: float = 0.1


@router.post("/process")
async def process_xrd(request: ProcessRequest):
    """
    对文本 XRD 数据做处理
    输入: { data: [[angle, intensity], ...], min_angle, max_angle, step, sigma }
    输出: { original: { angles, intensities }, processed: { angles, intensities } }
    """
    if not request.data:
        raise HTTPException(status_code=400, detail="XRD 数据不能为空")

    try:
        # 将对象列表转换为 numpy 数组 [N, 2]
        xrd_array = np.array([[p.angle, p.intensity] for p in request.data], dtype=np.float32)

        pos_emb, sign_emb = xrd_process(
            xrd_array,
            min_angle=request.min_angle,
            max_angle=request.max_angle,
            step=request.step,
            sigma=request.sigma,
        )

        # 生成用于绘图的网格角度
        grid_length = int((request.max_angle - request.min_angle) / request.step) + 1
        grid_angles = np.linspace(
            request.min_angle, request.max_angle, grid_length
        ).tolist()

        # 转换为可 JSON 序列化的列表
        broadened_intensities = sign_emb.squeeze().numpy().tolist()

        return {
            "original": {
                "angles": xrd_array[:, 0].tolist(),
                "intensities": xrd_array[:, 1].tolist(),
            },
            "processed": {
                "angles": grid_angles,
                "intensities": broadened_intensities,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@router.post("/upload-npy")
async def upload_npy(
    file: UploadFile = File(..., description="NPY 文件"),
    min_angle: float = Form(5.0),
    max_angle: float = Form(90.0),
    step: float = Form(0.01),
    sigma: float = Form(0.1),
):
    """
    上传 .npy 文件并处理 XRD 数据
    输入: FormData { file, min_angle, max_angle, step, sigma }
    输出: { original: { angles, intensities }, processed: { angles, intensities } }
    """
    if not file.filename or not file.filename.lower().endswith(".npy"):
        raise HTTPException(status_code=400, detail="请上传 .npy 文件")

    try:
        content = await file.read()
        buf = io.BytesIO(content)

        # 加载 NPY 文件
        arr = np.load(buf, allow_pickle=True)

        # 处理不同格式的 NPY 文件
        xrd_array = None

        # 处理 0 维对象（字典格式）
        if arr.ndim == 0:
            obj = arr.item()
            if isinstance(obj, dict) and "features" in obj:
                features = np.asarray(obj["features"], dtype=np.float32)
                # 取第一组数据
                if features.ndim == 2:
                    xrd_array = process_dense_features(features, min_angle, max_angle)
                else:
                    # 尝试作为原始数据
                    xrd_array = features.reshape(-1, 2) if features.size % 2 == 0 else None
            elif isinstance(obj, dict) and "data" in obj:
                xrd_array = np.asarray(obj["data"], dtype=np.float32)
            else:
                # 尝试直接转换
                xrd_array = np.asarray(obj, dtype=np.float32)
        # 处理 1 维数组
        elif arr.ndim == 1:
            # 可能是密集数据或需要配对
            if arr.size % 2 == 0:
                xrd_array = arr.reshape(-1, 2)
            else:
                # 假设是密集强度值，需要生成角度
                xrd_array = process_dense_data(arr, min_angle, max_angle)
        # 处理 2 维数组
        elif arr.ndim == 2:
            if arr.shape[1] == 2:
                # 已经是 [[angle, intensity], ...] 格式
                xrd_array = arr
            elif arr.shape[0] == 2:
                # 转置为 [[angle, intensity], ...] 格式
                xrd_array = arr.T
            else:
                # 假设是多组数据，取第一组
                xrd_array = process_dense_features(arr, min_angle, max_angle)

        if xrd_array is None or xrd_array.ndim != 2 or xrd_array.shape[1] != 2:
            raise HTTPException(status_code=400, detail="无法解析 NPY 文件格式")

        # 处理 XRD 数据
        pos_emb, sign_emb = xrd_process(
            xrd_array,
            min_angle=min_angle,
            max_angle=max_angle,
            step=step,
            sigma=sigma,
        )

        # 生成用于绘图的网格角度
        grid_length = int((max_angle - min_angle) / step) + 1
        grid_angles = np.linspace(min_angle, max_angle, grid_length).tolist()

        # 转换为可 JSON 序列化的列表
        broadened_intensities = sign_emb.squeeze().numpy().tolist()

        return {
            "original": {
                "angles": xrd_array[:, 0].tolist(),
                "intensities": xrd_array[:, 1].tolist(),
            },
            "processed": {
                "angles": grid_angles,
                "intensities": broadened_intensities,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


def process_dense_features(features, min_angle, max_angle):
    """
    将密集特征数据转换为 XRD 处理格式
    假设 features 是 [N, grid_points] 或 [grid_points] 格式
    """
    # 如果是 2D，取第一组
    if features.ndim == 2:
        data = features[0]
    else:
        data = features

    # 假设数据覆盖 min_angle 到 max_angle 的范围
    grid_points = data.shape[0]
    angles = np.linspace(min_angle, max_angle, grid_points)

    # 过滤掉接近零的值以提高效率
    threshold = 1e-6
    valid_mask = data > threshold

    if valid_mask.sum() == 0:
        return np.column_stack([angles, data])

    valid_angles = angles[valid_mask]
    valid_intensities = data[valid_mask]

    return np.column_stack([valid_angles, valid_intensities]).astype(np.float32)


def process_dense_data(data, min_angle, max_angle):
    """
    将 1D 密集数据转换为 XRD 处理格式
    """
    grid_points = data.shape[0]
    angles = np.linspace(min_angle, max_angle, grid_points)

    # 过滤掉接近零的值
    threshold = 1e-6
    valid_mask = data > threshold

    if valid_mask.sum() == 0:
        return np.column_stack([angles, data])

    valid_angles = angles[valid_mask]
    valid_intensities = data[valid_mask]

    return np.column_stack([valid_angles, valid_intensities]).astype(np.float32)
