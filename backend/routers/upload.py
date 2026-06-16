"""
文件上传模块路由
提供通用数据上传接口
"""

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import sqlite3
import uuid
from pathlib import Path
from datetime import datetime

router = APIRouter(tags=["Upload"])

# 数据库路径
DB_PATH = Path(__file__).resolve().parent.parent / "db_table" / "chemistry.db"

# 上传文件保存路径
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"


def get_db_path():
    """获取数据库路径"""
    return str(DB_PATH)


def ensure_upload_dir():
    """确保上传目录存在"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ========== 响应模型 ==========

class UploadResponse(BaseModel):
    success: bool
    fileId: str


# ========== 文件上传接口 ==========

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    通用数据上传接口
    - file: 上传的文件
    返回文件ID用于后续引用
    """
    ensure_upload_dir()

    # 生成唯一文件ID
    file_id = f"file-{uuid.uuid4().hex[:12]}"

    # 获取文件扩展名
    original_filename = file.filename or "unknown"
    file_ext = Path(original_filename).suffix

    # 构建保存路径
    save_filename = f"{file_id}{file_ext}"
    save_path = UPLOAD_DIR / save_filename

    try:
        # 保存文件
        content = await file.read()
        with open(save_path, "wb") as f:
            f.write(content)

        # 记录到数据库
        file_size = len(content)
        file_type = file.content_type or "application/octet-stream"
        upload_time = datetime.now().isoformat()

        with sqlite3.connect(get_db_path()) as conn:
            cursor = conn.cursor()
            # 使用 obs_files 表存储上传文件信息
            cursor.execute(
                """
                INSERT INTO obs_files (id, name, size, type, uploadTime, description)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (file_id, original_filename, file_size, file_type, upload_time, None)
            )
            conn.commit()

        return {
            "code": 200,
            "msg": None,
            "data": {
                "success": True,
                "fileId": file_id
            }
        }

    except Exception as e:
        # 如果保存失败，清理临时文件
        if save_path.exists():
            save_path.unlink()
        raise
