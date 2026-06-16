"""
分子开放检索模块路由
提供分子开放检索相关接口
"""

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import json
import uuid
import os
from datetime import datetime
from pathlib import Path

router = APIRouter(tags=["MoleculeOpen"])

# 数据库路径
DB_PATH = Path(__file__).resolve().parent.parent / "db_table" / "chemistry.db"
# 上传文件存储路径
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def get_db_path():
    """获取数据库路径"""
    return str(DB_PATH)


# ========== 请求模型 ==========

class CoreSearchRequest(BaseModel):
    page: int = 1
    size: int = 10
    keyword: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    formula: Optional[str] = None
    smiles: Optional[str] = None
    inchi: Optional[str] = None
    massMin: Optional[float] = None
    massMax: Optional[float] = None
    charge: Optional[int] = None
    spin: Optional[int] = None
    tags: Optional[List[str]] = None
    sortField: Optional[str] = None
    sortOrder: Optional[str] = "asc"


class SpectraTypeSearchRequest(BaseModel):
    spectraType: str
    page: int = 1
    size: int = 10


# ========== 核心/高级检索接口 ==========

@router.post("/molecule/open/search/core")
async def molecule_core_search(request: CoreSearchRequest):
    """
    分子核心/高级检索
    支持多条件组合查询和排序
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建查询条件
        conditions = []
        params = []

        # 关键词搜索（搜索多个字段）
        if request.keyword:
            conditions.append("""(
                inchikey LIKE ? OR
                smiles LIKE ? OR
                inchi LIKE ? OR
                iupac LIKE ? OR
                title LIKE ? OR
                molecularName LIKE ? OR
                displayFormula LIKE ?
            )""")
            like_keyword = f"%{request.keyword}%"
            params.extend([like_keyword] * 7)

        # 精确匹配字段
        if request.type:
            conditions.append("categoryObject = ?")
            params.append(request.type)

        if request.category:
            conditions.append("categoryLabel = ?")
            params.append(request.category)

        if request.formula:
            conditions.append("displayFormula LIKE ?")
            params.append(f"%{request.formula}%")

        if request.smiles:
            conditions.append("smiles LIKE ?")
            params.append(f"%{request.smiles}%")

        if request.inchi:
            conditions.append("inchi LIKE ?")
            params.append(f"%{request.inchi}%")

        # 数值范围
        if request.massMin is not None:
            conditions.append("exactMass >= ?")
            params.append(request.massMin)

        if request.massMax is not None:
            conditions.append("exactMass <= ?")
            params.append(request.massMax)

        if request.charge is not None:
            conditions.append("charge = ?")
            params.append(request.charge)

        # 构建 WHERE 子句
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        # 构建排序子句
        order_clause = "ORDER BY id DESC"  # 默认排序
        if request.sortField:
            valid_fields = ["id", "exactMass", "weight", "charge", "collectTime", "title"]
            if request.sortField in valid_fields:
                order_dir = "ASC" if request.sortOrder == "asc" else "DESC"
                order_clause = f"ORDER BY {request.sortField} {order_dir}"

        # 查询总数
        count_sql = f"SELECT COUNT(*) FROM molecules {where_clause}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()[0]

        # 查询当前页数据
        offset = (request.page - 1) * request.size
        data_sql = f"""
            SELECT id, inchikey, smiles, inchi, iupac, picId, title, molecularName,
                   displayFormula, exactMass, weight, charge, categoryLabel,
                   categoryObject, collectTime, author, cas, sourceResearchGroup
            FROM molecules
            {where_clause}
            {order_clause}
            LIMIT ? OFFSET ?
        """
        cursor.execute(data_sql, params + [request.size, offset])
        rows = cursor.fetchall()

        # 构建响应数据
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "inchikey": row["inchikey"] or "",
                "smiles": row["smiles"] or "",
                "inchi": row["inchi"] or "",
                "iupac": row["iupac"] or "",
                "picId": row["picId"] or "",
                "title": row["title"] or "",
                "molecularName": row["molecularName"] or "",
                "displayFormula": row["displayFormula"] or "",
                "exactMass": row["exactMass"],
                "weight": row["weight"],
                "charge": row["charge"],
                "categoryLabel": row["categoryLabel"] or "",
                "categoryObject": row["categoryObject"] or "",
                "collectTime": row["collectTime"],
                "author": row["author"] or "",
                "cas": row["cas"] or "",
                "sourceResearchGroup": row["sourceResearchGroup"] or ""
            })

        return {
            "code": 200,
            "msg": None,
            "data": {
                "result": result,
                "page": {
                    "size": request.size,
                    "current": request.page,
                    "total": total
                }
            }
        }


# ========== 按 picId 获取分子详情 ==========

@router.get("/molecule/open/{pic_id}")
async def get_molecule_by_pic_id(pic_id: str):
    """
    按 picId 获取分子详情
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM molecules WHERE picId = ?
            """,
            (pic_id,)
        )
        row = cursor.fetchone()

        if not row:
            return {
                "code": 404,
                "msg": "分子不存在",
                "data": None
            }

        # 构建完整的分子详情对象
        molecule = dict(row)

        # 处理可能为 JSON 的字段
        json_fields = ["tags", "atoms", "bonds"]
        for field in json_fields:
            if field in molecule and molecule[field]:
                try:
                    molecule[field] = json.loads(molecule[field])
                except (json.JSONDecodeError, TypeError):
                    molecule[field] = []
            else:
                molecule[field] = []

        return {
            "code": 200,
            "msg": None,
            "data": molecule
        }


# ========== 按分类统计分子数量 ==========

@router.get("/molecule/open/summary/groupbycategory")
async def get_molecule_summary_by_category():
    """
    按分类统计分子数量
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 优先从 category_summary 表读取
        cursor.execute(
            "SELECT category, count, percentage FROM category_summary ORDER BY count DESC"
        )
        rows = cursor.fetchall()

        if rows:
            result = [
                {
                    "category": row["category"],
                    "count": row["count"],
                    "percentage": row["percentage"]
                }
                for row in rows
            ]
        else:
            # 如果没有预存数据，则实时统计
            cursor.execute(
                """
                SELECT categoryLabel as category, COUNT(*) as count
                FROM molecules
                WHERE categoryLabel IS NOT NULL
                GROUP BY categoryLabel
                ORDER BY count DESC
                """
            )
            rows = cursor.fetchall()

            # 计算总数和百分比
            total = sum(row["count"] for row in rows)
            result = []
            for row in rows:
                count = row["count"]
                percentage = round(count / total * 100, 2) if total > 0 else 0
                result.append({
                    "category": row["category"],
                    "count": count,
                    "percentage": percentage
                })

        return {
            "code": 200,
            "msg": None,
            "data": result
        }


# ========== 分子总体统计 ==========

@router.get("/molecule/open/summary")
async def get_molecule_summary():
    """
    分子总体统计
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 优先从 molecule_summary 表读取
        cursor.execute(
            "SELECT title, description, category, updateTime FROM molecule_summary"
        )
        rows = cursor.fetchall()

        if rows:
            result = {
                "items": [
                    {
                        "title": row["title"],
                        "description": row["description"],
                        "category": row["category"],
                        "updateTime": row["updateTime"]
                    }
                    for row in rows
                ]
            }
        else:
            # 实时统计
            stats = {}

            # 总分子数
            cursor.execute("SELECT COUNT(*) as total FROM molecules")
            stats["totalMolecules"] = cursor.fetchone()["total"]

            # 有谱图的分子数
            cursor.execute("""
                SELECT COUNT(DISTINCT picId) as count
                FROM spectrum
                WHERE picId IN (SELECT picId FROM molecules WHERE picId IS NOT NULL)
            """)
            stats["moleculesWithSpectrum"] = cursor.fetchone()["count"]

            # 分类数量
            cursor.execute("SELECT COUNT(DISTINCT categoryLabel) as count FROM molecules WHERE categoryLabel IS NOT NULL")
            stats["categoryCount"] = cursor.fetchone()["count"]

            # 作者数量
            cursor.execute("SELECT COUNT(DISTINCT author) as count FROM molecules WHERE author IS NOT NULL")
            stats["authorCount"] = cursor.fetchone()["count"]

            # 谱图类型数量
            cursor.execute("SELECT COUNT(*) as count FROM spectrum_types")
            stats["spectrumTypeCount"] = cursor.fetchone()["count"]

            result = {
                "totalMolecules": stats.get("totalMolecules", 0),
                "moleculesWithSpectrum": stats.get("moleculesWithSpectrum", 0),
                "categoryCount": stats.get("categoryCount", 0),
                "authorCount": stats.get("authorCount", 0),
                "spectrumTypeCount": stats.get("spectrumTypeCount", 0)
            }

        return {
            "code": 200,
            "msg": None,
            "data": result
        }


# ========== 上传分子相关文件 ==========

@router.post("/molecule/open/upload")
async def upload_molecule_files(
    templateId: str = Form(...),
    tool: str = Form(...),
    metadata: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    上传分子相关文件
    - templateId: 模板ID
    - tool: 工具名称
    - metadata: 元数据JSON字符串
    - files: 上传的文件列表
    """
    try:
        # 解析元数据
        meta = json.loads(metadata) if metadata else {}

        # 保存文件
        saved_files = []
        for file in files:
            # 生成唯一文件名
            file_ext = Path(file.filename).suffix
            unique_name = f"{uuid.uuid4().hex}{file_ext}"
            file_path = UPLOAD_DIR / unique_name

            # 保存文件内容
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)

            saved_files.append({
                "originalName": file.filename,
                "savedName": unique_name,
                "size": len(content),
                "path": str(file_path)
            })

        # 生成上传记录ID
        upload_id = f"upload-{uuid.uuid4().hex[:8]}"

        return {
            "code": 200,
            "msg": None,
            "data": {
                "success": True,
                "uploadId": upload_id,
                "fileCount": len(saved_files),
                "files": saved_files
            }
        }

    except json.JSONDecodeError:
        return {
            "code": 400,
            "msg": "无效的元数据格式",
            "data": None
        }
    except Exception as e:
        return {
            "code": 500,
            "msg": f"上传失败: {str(e)}",
            "data": None
        }


# ========== 获取分子谱图数据 ==========

@router.get("/molecule/open/spectrum/{pic_id}")
async def get_molecule_spectrum(pic_id: str):
    """
    获取分子谱图数据
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, picId, type, name, instrument, conditions, xLabel, yLabel, peaks, dataPoints
            FROM spectrum
            WHERE picId = ?
            """,
            (pic_id,)
        )
        rows = cursor.fetchall()

        result = []
        for row in rows:
            spectrum_data = {
                "id": row["id"],
                "picId": row["picId"],
                "type": row["type"] or "",
                "name": row["name"] or "",
                "instrument": row["instrument"] or "",
                "conditions": row["conditions"] or "",
                "xLabel": row["xLabel"] or "",
                "yLabel": row["yLabel"] or ""
            }

            # 解析 JSON 字段
            try:
                if row["peaks"]:
                    spectrum_data["peaks"] = json.loads(row["peaks"])
                else:
                    spectrum_data["peaks"] = []
            except (json.JSONDecodeError, TypeError):
                spectrum_data["peaks"] = []

            try:
                if row["dataPoints"]:
                    spectrum_data["dataPoints"] = json.loads(row["dataPoints"])
                else:
                    spectrum_data["dataPoints"] = []
            except (json.JSONDecodeError, TypeError):
                spectrum_data["dataPoints"] = []

            result.append(spectrum_data)

        return {
            "code": 200,
            "msg": None,
            "data": result
        }


# ========== 按谱学类型检索分子 ==========

@router.post("/molecule/open/search/by-spectra-type")
async def search_molecule_by_spectra_type(request: SpectraTypeSearchRequest):
    """
    按谱学类型检索分子
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 先查询具有该谱学类型的 picId 列表
        cursor.execute(
            "SELECT DISTINCT picId FROM spectrum WHERE type = ?",
            (request.spectraType,)
        )
        pic_ids = [row["picId"] for row in cursor.fetchall()]

        if not pic_ids:
            return {
                "code": 200,
                "msg": None,
                "data": {
                    "result": [],
                    "page": {
                        "size": request.size,
                        "current": request.page,
                        "total": 0
                    }
                }
            }

        # 构建 IN 子句
        placeholders = ",".join(["?"] * len(pic_ids))

        # 查询总数
        cursor.execute(
            f"SELECT COUNT(*) FROM molecules WHERE picId IN ({placeholders})",
            pic_ids
        )
        total = cursor.fetchone()[0]

        # 分页查询分子数据
        offset = (request.page - 1) * request.size
        cursor.execute(
            f"""
            SELECT id, inchikey, smiles, inchi, iupac, picId, title, molecularName,
                   displayFormula, exactMass, weight, charge, categoryLabel, categoryObject
            FROM molecules
            WHERE picId IN ({placeholders})
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            pic_ids + [request.size, offset]
        )
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "inchikey": row["inchikey"] or "",
                "smiles": row["smiles"] or "",
                "inchi": row["inchi"] or "",
                "iupac": row["iupac"] or "",
                "picId": row["picId"] or "",
                "title": row["title"] or "",
                "molecularName": row["molecularName"] or "",
                "displayFormula": row["displayFormula"] or "",
                "exactMass": row["exactMass"],
                "weight": row["weight"],
                "charge": row["charge"],
                "categoryLabel": row["categoryLabel"] or "",
                "categoryObject": row["categoryObject"] or ""
            })

        return {
            "code": 200,
            "msg": None,
            "data": {
                "result": result,
                "page": {
                    "size": request.size,
                    "current": request.page,
                    "total": total
                }
            }
        }


# ========== 上传 OBS 文件 ==========

@router.post("/molecule/open/obs-files")
async def upload_obs_file(
    file: UploadFile = File(...),
    moleculeId: Optional[str] = Form(None),
    description: Optional[str] = Form(None)
):
    """
    上传 OBS 文件
    """
    try:
        # 生成 OBS 文件ID
        file_id = f"obs-{uuid.uuid4().hex[:8]}"

        # 保存文件
        file_ext = Path(file.filename).suffix
        unique_name = f"{file_id}{file_ext}"
        file_path = UPLOAD_DIR / unique_name

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # 记录到数据库
        upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect(get_db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO obs_files (id, name, size, type, uploadTime, moleculeId, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (file_id, file.filename, len(content), file.content_type, upload_time, moleculeId, description)
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
        return {
            "code": 500,
            "msg": f"上传失败: {str(e)}",
            "data": None
        }


# ========== 获取 OBS 文件下载信息 ==========

@router.get("/molecule/open/obs-files/download")
async def get_obs_file_download_info(fileId: str):
    """
    获取 OBS 文件下载信息
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM obs_files WHERE id = ?",
            (fileId,)
        )
        row = cursor.fetchone()

        if not row:
            return {
                "code": 404,
                "msg": "文件不存在",
                "data": None
            }

        # 构建下载 URL
        file_name = f"{row['id']}{Path(row['name']).suffix}"
        file_path = UPLOAD_DIR / file_name

        if not file_path.exists():
            return {
                "code": 404,
                "msg": "文件已丢失",
                "data": None
            }

        return {
            "code": 200,
            "msg": None,
            "data": {
                "fileId": row["id"],
                "name": row["name"],
                "size": row["size"],
                "type": row["type"],
                "uploadTime": row["uploadTime"],
                "downloadUrl": f"/api/molecule/open/obs-files/download/{row['id']}",
                "description": row["description"] or ""
            }
        }


# ========== 获取 OBS 文件预览/流式内容 ==========

@router.get("/molecule/open/obs-files/stream")
async def get_obs_file_stream(fileId: str):
    """
    获取 OBS 文件预览/流式内容
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM obs_files WHERE id = ?",
            (fileId,)
        )
        row = cursor.fetchone()

        if not row:
            return {
                "code": 404,
                "msg": "文件不存在",
                "data": None
            }

        # 读取文件内容
        file_name = f"{row['id']}{Path(row['name']).suffix}"
        file_path = UPLOAD_DIR / file_name

        if not file_path.exists():
            return {
                "code": 404,
                "msg": "文件已丢失",
                "data": None
            }

        # 读取文件内容（限制预览大小）
        try:
            with open(file_path, "rb") as f:
                content = f.read()

            # 根据文件类型决定预览方式
            file_type = row["type"] or ""
            preview_type = "binary"
            preview_content = None

            if file_type.startswith("text/") or file_type in ["application/json", "application/xml"]:
                preview_type = "text"
                try:
                    preview_content = content.decode("utf-8")[:5000]  # 限制文本预览大小
                except UnicodeDecodeError:
                    preview_type = "binary"
            elif file_type.startswith("image/"):
                preview_type = "image"
                import base64
                preview_content = base64.b64encode(content).decode("utf-8")

            return {
                "code": 200,
                "msg": None,
                "data": {
                    "fileId": row["id"],
                    "name": row["name"],
                    "size": row["size"],
                    "type": row["type"],
                    "previewType": preview_type,
                    "previewContent": preview_content,
                    "isTruncated": len(content) > 5000 if preview_type == "text" else False
                }
            }

        except Exception as e:
            return {
                "code": 500,
                "msg": f"读取文件失败: {str(e)}",
                "data": None
            }
