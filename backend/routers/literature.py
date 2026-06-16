"""
文献模块路由
提供文献相关的查询接口
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
from pathlib import Path

router = APIRouter(tags=["Literature"])

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


class LiteratureItem(BaseModel):
    id: int
    doi: Optional[str] = None
    title: str
    authors: Optional[str] = None
    journal: Optional[str] = None
    year: Optional[int] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[str] = None
    tags: Optional[str] = None


class LiteratureListResponse(BaseModel):
    result: List[LiteratureItem]
    page: PageInfo


class LiteratureDetail(BaseModel):
    id: int
    doi: Optional[str] = None
    title: str
    authors: Optional[str] = None
    journal: Optional[str] = None
    year: Optional[int] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[str] = None
    tags: Optional[str] = None


# ========== 文献相关接口 ==========

@router.get("/literature")
async def get_literature_list(
    page: int = 1,
    size: int = 10,
    keyword: Optional[str] = None
):
    """
    获取文献列表
    - page: 页码（从1开始）
    - size: 每页数量
    - keyword: 搜索关键词（可选）
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建查询条件
        where_clause = ""
        params = []
        if keyword:
            where_clause = "WHERE title LIKE ? OR authors LIKE ? OR abstract LIKE ? OR keywords LIKE ?"
            like_keyword = f"%{keyword}%"
            params = [like_keyword, like_keyword, like_keyword, like_keyword]

        # 查询总数
        count_sql = f"SELECT COUNT(*) FROM literature {where_clause}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()[0]

        # 查询当前页数据
        offset = (page - 1) * size
        data_sql = f"""
            SELECT id, doi, title, authors, journal, year, volume, issue, pages, abstract, keywords, tags
            FROM literature
            {where_clause}
            ORDER BY year DESC, id DESC
            LIMIT ? OFFSET ?
        """
        cursor.execute(data_sql, params + [size, offset])
        rows = cursor.fetchall()

        # 构建响应数据
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "doi": row["doi"] or "",
                "title": row["title"] or "",
                "authors": row["authors"] or "",
                "journal": row["journal"] or "",
                "year": row["year"],
                "volume": row["volume"] or "",
                "issue": row["issue"] or "",
                "pages": row["pages"] or "",
                "abstract": row["abstract"] or "",
                "keywords": row["keywords"] or "",
                "tags": row["tags"] or ""
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


@router.get("/literature/{literature_id}")
async def get_literature_detail(literature_id: int):
    """
    获取文献详情
    - literature_id: 文献ID
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, doi, title, authors, journal, year, volume, issue, pages, abstract, keywords, tags
            FROM literature WHERE id = ?
            """,
            (literature_id,)
        )
        row = cursor.fetchone()

        if not row:
            return {
                "code": 404,
                "msg": "文献不存在",
                "data": None
            }

        return {
            "code": 200,
            "msg": None,
            "data": {
                "id": row["id"],
                "doi": row["doi"] or "",
                "title": row["title"] or "",
                "authors": row["authors"] or "",
                "journal": row["journal"] or "",
                "year": row["year"],
                "volume": row["volume"] or "",
                "issue": row["issue"] or "",
                "pages": row["pages"] or "",
                "abstract": row["abstract"] or "",
                "keywords": row["keywords"] or "",
                "tags": row["tags"] or ""
            }
        }
