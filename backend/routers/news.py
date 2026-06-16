"""
新闻公告模块路由
提供新闻和公告的查询接口
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any
import sqlite3
from pathlib import Path

router = APIRouter(tags=["News"])

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


class NewsItem(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    author: Optional[str] = None
    summary: Optional[str] = None
    createTime: Optional[str] = None


class NewsListResponse(BaseModel):
    result: List[NewsItem]
    page: PageInfo


class AnnouncementItem(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    author: Optional[str] = None
    importance: Optional[str] = None
    createTime: Optional[str] = None


class AnnouncementListResponse(BaseModel):
    result: List[AnnouncementItem]
    page: PageInfo


# ========== 新闻相关接口 ==========

@router.get("/news")
async def get_news_list(
    page: int = 1,
    size: int = 10,
    keyword: Optional[str] = None
):
    """
    获取新闻列表
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
            where_clause = "WHERE title LIKE ? OR content LIKE ? OR summary LIKE ?"
            like_keyword = f"%{keyword}%"
            params = [like_keyword, like_keyword, like_keyword]

        # 查询总数
        count_sql = f"SELECT COUNT(*) FROM news {where_clause}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()[0]

        # 查询当前页数据
        offset = (page - 1) * size
        data_sql = f"""
            SELECT id, title, content, author, summary, createTime
            FROM news
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
                "title": row["title"] or "",
                "content": row["content"] or "",
                "author": row["author"] or "",
                "summary": row["summary"] or "",
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


@router.get("/news/{news_id}")
async def get_news_detail(news_id: int):
    """
    获取新闻详情
    - news_id: 新闻ID
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, title, content, author, summary, createTime FROM news WHERE id = ?",
            (news_id,)
        )
        row = cursor.fetchone()

        if not row:
            return {
                "code": 404,
                "msg": "新闻不存在",
                "data": None
            }

        return {
            "code": 200,
            "msg": None,
            "data": {
                "id": row["id"],
                "title": row["title"] or "",
                "content": row["content"] or "",
                "author": row["author"] or "",
                "summary": row["summary"] or "",
                "createTime": row["createTime"] or ""
            }
        }


# ========== 公告相关接口 ==========

@router.get("/announcements")
async def get_announcements_list(
    page: int = 1,
    size: int = 10
):
    """
    获取公告列表
    - page: 页码（从1开始）
    - size: 每页数量
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 查询总数
        cursor.execute("SELECT COUNT(*) FROM announcements")
        total = cursor.fetchone()[0]

        # 查询当前页数据
        offset = (page - 1) * size
        cursor.execute(
            """
            SELECT id, title, content, author, importance, createTime
            FROM announcements
            ORDER BY createTime DESC, id DESC
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
                "title": row["title"] or "",
                "content": row["content"] or "",
                "author": row["author"] or "",
                "importance": row["importance"] or "",
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


@router.get("/announcements/{announcement_id}")
async def get_announcement_detail(announcement_id: int):
    """
    获取公告详情
    - announcement_id: 公告ID
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, title, content, author, importance, createTime FROM announcements WHERE id = ?",
            (announcement_id,)
        )
        row = cursor.fetchone()

        if not row:
            return {
                "code": 404,
                "msg": "公告不存在",
                "data": None
            }

        return {
            "code": 200,
            "msg": None,
            "data": {
                "id": row["id"],
                "title": row["title"] or "",
                "content": row["content"] or "",
                "author": row["author"] or "",
                "importance": row["importance"] or "",
                "createTime": row["createTime"] or ""
            }
        }
