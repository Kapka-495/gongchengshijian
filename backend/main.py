"""
材料可视化 - 后端 API
提供 XRD 数据处理与可视化数据接口
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from typing import List, Optional
import io
import numpy as np
import os
import tempfile

from xrd_processor import xrd_process

app = FastAPI(title="材料 XRD 可视化", version="1.0.0")

# Global cache for loaded NPY data
_npy_cache = {}

# 挂载前端静态文件（若 frontend 目录存在）
_frontend_path = Path(__file__).resolve().parent.parent / "frontend"
if _frontend_path.exists():
    app.mount("/static", StaticFiles(directory=_frontend_path), name="static")

# 允许跨域请求（前后端分离）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class XRDDataPoint(BaseModel):
    angle: float  # 2-theta 角度 (度)
    intensity: float  # 强度


class ProcessRequest(BaseModel):
    data: List[XRDDataPoint]  # XRD 原始数据
    min_angle: float = 5.0
    max_angle: float = 90.0
    step: float = 0.01
    sigma: float = 0.1


@app.get("/")
async def root():
    """根路径：若存在前端则返回首页，否则返回 API 信息"""
    index_file = _frontend_path / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "材料 XRD 可视化 API", "docs": "/docs"}


@app.post("/api/process")
async def process_xrd(request: ProcessRequest):
    """
    处理 XRD 数据，返回展宽后的稠密向量用于可视化
    """
    if not request.data:
        raise HTTPException(status_code=400, detail="XRD 数据不能为空")

    try:
        # 转换为 numpy 数组 [N, 2]
        xrd_array = np.array(
            [[p.angle, p.intensity] for p in request.data], dtype=np.float32
        )

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
                "angles": [p.angle for p in request.data],
                "intensities": [p.intensity for p in request.data],
            },
            "processed": {
                "angles": grid_angles,
                "intensities": broadened_intensities,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@app.post("/api/upload-npy")
async def upload_npy_file(
    file: UploadFile = File(..., description="NPY 文件，包含 features 和 labels230 键"),
):
    """
    上传并缓存 NPY 文件，返回可用数据组信息
    """
    if not file.filename or not file.filename.lower().endswith(".npy"):
        raise HTTPException(status_code=400, detail="请上传 .npy 文件")

    try:
        content = await file.read()
        buf = io.BytesIO(content)

        # Load NPY file with pickle support for dictionary format
        arr = np.load(buf, allow_pickle=True)

        # Handle 0-dimensional object (dictionary format)
        if arr.ndim == 0:
            obj = arr.item()
            if isinstance(obj, dict) and "features" in obj:
                features = np.asarray(obj["features"], dtype=np.float32)
                if features.ndim != 2:
                    raise HTTPException(
                        status_code=400,
                        detail=f"features 应为二维数组 (样本数, 网格点数)，当前形状: {features.shape}",
                    )

                # Cache the features array using a unique key to avoid conflicts
                import uuid
                cache_key = f"{file.filename}_{uuid.uuid4().hex[:8]}"
                _npy_cache[cache_key] = features
                print(f"调试: 缓存文件 '{file.filename}' -> '{cache_key}', 总缓存数: {len(_npy_cache)}")

                return {
                    "success": True,
                    "filename": cache_key,  # Return the unique cache key
                    "total_groups": features.shape[0],
                    "grid_points": features.shape[1],
                    "message": f"成功加载 {features.shape[0]} 组数据，每组 {features.shape[1]} 个网格点"
                }
            else:
                raise HTTPException(
                    status_code=400,
                    detail="NPY 文件必须包含 'features' 键",
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="不支持的 NPY 格式，期望 0 维对象包含 features 键",
            )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"无法解析 NPY 文件: {str(e)}")


@app.post("/api/process-npy-group")
async def process_npy_group(
    filename: str = Form(..., description="已上传的 NPY 文件名"),
    group_index: int = Form(..., description="要选择的数据组索引 (0-based)"),
    min_angle: float = Form(5.0),
    max_angle: float = Form(90.0),
):
    """
    处理已上传 NPY 文件中的指定数据组
    """
    print(f"调试: 查找缓存文件 '{filename}', 当前缓存键: {list(_npy_cache.keys())}")
    if filename not in _npy_cache:
        raise HTTPException(status_code=404, detail=f"文件 '{filename}' 未找到，请重新上传。可用缓存: {list(_npy_cache.keys())}")

    features = _npy_cache[filename]

    if group_index < 0 or group_index >= features.shape[0]:
        raise HTTPException(
            status_code=400,
            detail=f"数据组索引超出范围，可用范围: 0-{features.shape[0]-1}"
        )

    try:
        # Extract the selected group data
        group_data = features[group_index, :]  # Shape: (8500,)

        # Create angles array (5-90 degrees, 0.01 degree step = 8500 points)
        angles = np.linspace(5.0, 90.0, 8500)

        # Create the expected format for xrd_process: [N, 2] array
        # Since this is already dense data, we'll treat each point as a peak
        # But we need to filter out near-zero intensities to avoid excessive processing
        threshold = 1e-6
        valid_mask = group_data > threshold

        if valid_mask.sum() == 0:
            # If all values are near zero, return zeros
            grid_length = int((max_angle - min_angle) / 0.01) + 1
            grid_angles = np.linspace(min_angle, max_angle, grid_length).tolist()
            zero_intensities = [0.0] * grid_length

            return {
                "original": {"angles": [], "intensities": []},
                "processed": {"angles": grid_angles, "intensities": zero_intensities},
            }

        valid_angles = angles[valid_mask]
        valid_intensities = group_data[valid_mask]

        # Create [N, 2] array for processing
        xrd_array = np.column_stack([valid_angles, valid_intensities]).astype(np.float32)

        # Process using the existing xrd_process function
        pos_emb, sign_emb = xrd_process(
            xrd_array,
            min_angle=min_angle,
            max_angle=max_angle,
            step=0.01,  # Fixed step for 8500 points over 85 degrees
            sigma=0.1,
        )

        # Generate output grid
        grid_length = int((max_angle - min_angle) / 0.01) + 1
        grid_angles = np.linspace(min_angle, max_angle, grid_length).tolist()
        broadened_intensities = sign_emb.squeeze().numpy().tolist()

        return {
            "original": {
                "angles": valid_angles.tolist(),
                "intensities": valid_intensities.tolist(),
            },
            "processed": {
                "angles": grid_angles,
                "intensities": broadened_intensities,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@app.get("/api/npy-info/{filename}")
async def get_npy_info(filename: str):
    """
    获取已上传 NPY 文件的信息
    """
    if filename not in _npy_cache:
        raise HTTPException(status_code=404, detail="文件未找到")

    features = _npy_cache[filename]
    return {
        "filename": filename,
        "total_groups": features.shape[0],
        "grid_points": features.shape[1],
        "shape": features.shape,
        "dtype": str(features.dtype)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
