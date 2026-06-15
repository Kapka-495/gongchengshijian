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

from xrd_processor import xrd_process

app = FastAPI(title="材料 XRD 可视化", version="1.0.0")

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


@app.post("/api/process-npy")
async def process_xrd_npy(
    file: UploadFile = File(..., description="NPY 文件，形状 [N, 2]，第 0 列为 2θ 角度、第 1 列为强度"),
    min_angle: float = Form(5.0),
    max_angle: float = Form(90.0),
    step: float = Form(0.01),
    sigma: float = Form(0.1),
):
    """
    上传 .npy 文件处理 XRD 数据。NPY 数组应为 shape (N, 2)，列依次为角度(度)、强度。
    """
    if not file.filename or not file.filename.lower().endswith(".npy"):
        raise HTTPException(status_code=400, detail="请上传 .npy 文件")

    try:
        content = await file.read()
        buf = io.BytesIO(content)
        try:
            arr = np.load(buf, allow_pickle=False)
        except ValueError as e:
            if "allow_pickle" in str(e).lower():
                buf.seek(0)
                arr = np.load(buf, allow_pickle=True)
            else:
                raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"无法解析 NPY 文件: {str(e)}")

    # 支持 CoreMOF 等格式：0 维对象，内含 'features' 为 (n_samples, n_grid) 的稠密 XRD 曲线
    if arr.ndim == 0:
        obj = arr.item()
        if isinstance(obj, dict) and "features" in obj:
            features = np.asarray(obj["features"], dtype=np.float32)
            if features.ndim != 2 or features.shape[1] < 2:
                raise HTTPException(
                    status_code=400,
                    detail=f"features 应为二维数组 (样本数, 网格点数)，当前形状: {features.shape}",
                )
            n_grid = features.shape[1]
            angles = np.linspace(min_angle, max_angle, n_grid).tolist()
            # 取第一条曲线（第一个样本）用于可视化
            intensities = features[0, :].tolist()
            # 稠密数据无需再展宽，原始与处理结果一致
            return {
                "original": {"angles": angles, "intensities": intensities},
                "processed": {"angles": angles, "intensities": intensities},
            }
        raise HTTPException(
            status_code=400,
            detail="NPY 为 0 维对象但未包含 'features' 键，或格式不支持",
        )

    if arr.ndim != 2 or arr.shape[1] < 2:
        raise HTTPException(
            status_code=400,
            detail=f"NPY 数组应为二维且至少两列 (角度, 强度)，当前形状: {arr.shape}",
        )

    xrd_array = np.asarray(arr[:, :2], dtype=np.float32)

    try:
        pos_emb, sign_emb = xrd_process(
            xrd_array,
            min_angle=min_angle,
            max_angle=max_angle,
            step=step,
            sigma=sigma,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

    grid_length = int((max_angle - min_angle) / step) + 1
    grid_angles = np.linspace(min_angle, max_angle, grid_length).tolist()
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
