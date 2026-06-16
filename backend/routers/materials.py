"""
材料模块路由
提供材料相关的查询接口
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
from pathlib import Path

router = APIRouter(tags=["Materials"])

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


class MaterialItem(BaseModel):
    id: int
    name: str
    formula: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[str] = None
    bandGap: Optional[float] = None
    latticeConstant: Optional[float] = None
    crystalSystem: Optional[str] = None
    spaceGroup: Optional[str] = None
    createTime: Optional[str] = None


class MaterialListResponse(BaseModel):
    result: List[MaterialItem]
    page: PageInfo


class MaterialDetail(BaseModel):
    id: int
    name: str
    formula: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[str] = None
    bandGap: Optional[float] = None
    latticeConstant: Optional[float] = None
    crystalSystem: Optional[str] = None
    spaceGroup: Optional[str] = None
    createTime: Optional[str] = None


class TagItem(BaseModel):
    id: int
    name: str
    count: int
    category: Optional[str] = None


# ========== 材料相关接口 ==========

@router.get("/materials")
async def get_materials_list(
    page: int = 1,
    size: int = 10,
    keyword: Optional[str] = None,
    type: Optional[str] = None
):
    """
    获取材料列表
    - page: 页码（从1开始）
    - size: 每页数量
    - keyword: 搜索关键词（可选）
    - type: 材料类型筛选（可选）
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建查询条件
        where_clauses = []
        params = []
        if keyword:
            where_clauses.append("(name LIKE ? OR formula LIKE ? OR tags LIKE ?)")
            like_keyword = f"%{keyword}%"
            params.extend([like_keyword, like_keyword, like_keyword])
        if type:
            where_clauses.append("type = ?")
            params.append(type)

        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

        # 查询总数
        count_sql = f"SELECT COUNT(*) FROM materials {where_clause}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()[0]

        # 查询当前页数据
        offset = (page - 1) * size
        data_sql = f"""
            SELECT id, name, formula, type, tags, bandGap, latticeConstant,
                   crystalSystem, spaceGroup, createTime
            FROM materials
            {where_clause}
            ORDER BY createTime DESC, id DESC
            LIMIT ? OFFSET ?
        """
        cursor.execute(data_sql, params + [size, offset])
        rows = cursor.fetchall()

        # 构建响应数据
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "name": row["name"] or "",
                "formula": row["formula"] or "",
                "type": row["type"] or "",
                "tags": row["tags"] or "",
                "bandGap": row["bandGap"],
                "latticeConstant": row["latticeConstant"],
                "crystalSystem": row["crystalSystem"] or "",
                "spaceGroup": row["spaceGroup"] or "",
                "createTime": row["createTime"] or ""
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


@router.get("/materials/tags")
async def get_material_tags():
    """
    获取材料标签列表
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, count, category
            FROM material_tags
            ORDER BY count DESC, name ASC
            """
        )
        rows = cursor.fetchall()

        # 构建响应数据
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "name": row["name"] or "",
                "count": row["count"] or 0,
                "category": row["category"] or ""
            })

        return {
            "code": 200,
            "msg": None,
            "data": result
        }


@router.get("/materials/{material_id}")
async def get_material_detail(material_id: int):
    """
    获取材料详情
    - material_id: 材料ID
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, formula, type, tags, bandGap, latticeConstant,
                   crystalSystem, spaceGroup, createTime
            FROM materials WHERE id = ?
            """,
            (material_id,)
        )
        row = cursor.fetchone()

        if not row:
            return {
                "code": 404,
                "msg": "材料不存在",
                "data": None
            }

        return {
            "code": 200,
            "msg": None,
            "data": {
                "id": row["id"],
                "name": row["name"] or "",
                "formula": row["formula"] or "",
                "type": row["type"] or "",
                "tags": row["tags"] or "",
                "bandGap": row["bandGap"],
                "latticeConstant": row["latticeConstant"],
                "crystalSystem": row["crystalSystem"] or "",
                "spaceGroup": row["spaceGroup"] or "",
                "createTime": row["createTime"] or ""
            }
        }
