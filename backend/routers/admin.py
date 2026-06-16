"""
管理后台模块路由
提供审计日志、元数据管理接口
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
from pathlib import Path

router = APIRouter(tags=["Admin"])

# 数据库路径
DB_PATH = Path(__file__).resolve().parent.parent / "db_table" / "chemistry.db"


def get_db_path():
    """获取数据库路径"""
    return str(DB_PATH)


# ========== 响应模型 ==========

class PageInfo(BaseModel):
    size: int
    current: int
    total: int


class AuditLogItem(BaseModel):
    id: int
    userId: int
    username: str
    action: Optional[str] = None
    resource: Optional[str] = None
    detail: Optional[str] = None
    ip: Optional[str] = None
    time: Optional[str] = None


class AuditLogListResponse(BaseModel):
    result: List[AuditLogItem]
    page: PageInfo


class MetadataItem(BaseModel):
    id: int
    fieldEn: str
    fieldZh: Optional[str] = None
    type: Optional[str] = None
    required: bool = False
    description: Optional[str] = None


class MetadataListResponse(BaseModel):
    result: List[MetadataItem]
    page: PageInfo


class MetadataCreateRequest(BaseModel):
    fieldEn: str
    fieldZh: Optional[str] = None
    type: Optional[str] = None
    required: bool = False
    description: Optional[str] = None


class MetadataCreateResponse(BaseModel):
    success: bool
    id: int


class DeleteResponse(BaseModel):
    success: bool


# ========== 审计日志相关接口 ==========

@router.get("/admin/audit-logs")
async def get_audit_logs_list(
    page: int = 1,
    size: int = 10
):
    """
    获取系统审计日志列表
    - page: 页码（从1开始）
    - size: 每页数量
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 查询总数
        cursor.execute("SELECT COUNT(*) FROM audit_logs")
        total = cursor.fetchone()[0]

        # 查询当前页数据
        offset = (page - 1) * size
        cursor.execute(
            """
            SELECT id, userId, username, action, resource, detail, ip, time
            FROM audit_logs
            ORDER BY time DESC, id DESC
            LIMIT ? OFFSET ?
            """,
            (size, offset)
        )
        rows = cursor.fetchall()

        # 构建响应数据
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "userId": row["userId"],
                "username": row["username"] or "",
                "action": row["action"] or "",
                "resource": row["resource"] or "",
                "detail": row["detail"] or "",
                "ip": row["ip"] or "",
                "time": row["time"] or ""
            })

        return {
            "code": 200,
            "msg": None,
            "data": {
                "result": result,
                "page": {
                    "size": size,
                    "current": page,
                    "total": total
                }
            }
        }


# ========== 元数据相关接口 ==========

@router.get("/admin/metadata")
async def get_metadata_list(
    page: int = 1,
    size: int = 10
):
    """
    获取元数据列表
    - page: 页码（从1开始）
    - size: 每页数量
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 查询总数
        cursor.execute("SELECT COUNT(*) FROM metadata")
        total = cursor.fetchone()[0]

        # 查询当前页数据
        offset = (page - 1) * size
        cursor.execute(
            """
            SELECT id, fieldEn, fieldZh, type, required, description
            FROM metadata
            ORDER BY id ASC
            LIMIT ? OFFSET ?
            """,
            (size, offset)
        )
        rows = cursor.fetchall()

        # 构建响应数据
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "fieldEn": row["fieldEn"] or "",
                "fieldZh": row["fieldZh"] or "",
                "type": row["type"] or "",
                "required": bool(row["required"]),
                "description": row["description"] or ""
            })

        return {
            "code": 200,
            "msg": None,
            "data": {
                "result": result,
                "page": {
                    "size": size,
                    "current": page,
                    "total": total
                }
            }
        }


@router.post("/admin/metadata")
async def create_or_update_metadata(metadata: MetadataCreateRequest):
    """
    新增或保存元数据
    如果 fieldEn 已存在则更新，否则新增
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 检查是否已存在
        cursor.execute(
            "SELECT id FROM metadata WHERE fieldEn = ?",
            (metadata.fieldEn,)
        )
        existing = cursor.fetchone()

        required_int = 1 if metadata.required else 0

        if existing:
            # 更新现有记录
            cursor.execute(
                """
                UPDATE metadata
                SET fieldZh = ?, type = ?, required = ?, description = ?
                WHERE fieldEn = ?
                """,
                (metadata.fieldZh, metadata.type, required_int, metadata.description, metadata.fieldEn)
            )
            metadata_id = existing["id"]
        else:
            # 插入新记录
            cursor.execute(
                """
                INSERT INTO metadata (fieldEn, fieldZh, type, required, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                (metadata.fieldEn, metadata.fieldZh, metadata.type, required_int, metadata.description)
            )
            metadata_id = cursor.lastrowid

        conn.commit()

        return {
            "code": 200,
            "msg": None,
            "data": {
                "success": True,
                "id": metadata_id
            }
        }


@router.delete("/admin/metadata/{metadata_id}")
async def delete_metadata(metadata_id: int):
    """
    删除元数据
    - metadata_id: 元数据ID
    """
    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM metadata WHERE id = ?",
            (metadata_id,)
        )
        conn.commit()

        return {
            "code": 200,
            "msg": None,
            "data": {
                "success": True
            }
        }
