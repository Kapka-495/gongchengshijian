"""
分子模块路由
提供分子相关的查询接口
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import json
from pathlib import Path

router = APIRouter(tags=["Molecule"])

# 数据库路径
DB_PATH = Path(__file__).resolve().parent.parent / "db_table" / "chemistry.db"


def get_db_path():
    """获取数据库路径"""
    return str(DB_PATH)


# ========== 请求/响应模型 ==========

class SimilarityRequest(BaseModel):
    smiles: str
    type: Optional[str] = "2d"  # 默认为 2d
    threshold: Optional[float] = 0.7  # 默认为 0.7


# ========== 分子列表接口 ==========

@router.get("/molecule/list")
async def get_molecule_list(
    page: int = 1,
    size: int = 10,
    keyword: Optional[str] = None,
    type: Optional[str] = None
):
    """
    获取分子列表
    - page: 页码（从1开始）
    - size: 每页数量
    - keyword: 搜索关键词（可选，搜索 formula, smiles, inchi）
    - type: 分子类型筛选（可选）
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建查询条件
        conditions = []
        params = []

        if keyword:
            conditions.append("(formula LIKE ? OR smiles LIKE ? OR inchi LIKE ?)")
            like_keyword = f"%{keyword}%"
            params.extend([like_keyword, like_keyword, like_keyword])

        if type:
            conditions.append("type = ?")
            params.append(type)

        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        # 查询总数
        count_sql = f"SELECT COUNT(*) FROM molecules {where_clause}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()[0]

        # 查询当前页数据
        offset = (page - 1) * size
        data_sql = f"""
            SELECT id, formula, smiles, inchi, mass, volume, type, tags, charge, spin, atoms, bonds, createTime
            FROM molecules
            {where_clause}
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """
        cursor.execute(data_sql, params + [size, offset])
        rows = cursor.fetchall()

        # 构建响应数据
        result = []
        for row in rows:
            # 解析 tags, atoms, bonds JSON 字符串
            tags = []
            atoms = []
            bonds = []

            try:
                if row["tags"]:
                    tags = json.loads(row["tags"])
            except (json.JSONDecodeError, TypeError):
                pass

            try:
                if row["atoms"]:
                    atoms = json.loads(row["atoms"])
            except (json.JSONDecodeError, TypeError):
                pass

            try:
                if row["bonds"]:
                    bonds = json.loads(row["bonds"])
            except (json.JSONDecodeError, TypeError):
                pass

            result.append({
                "id": row["id"],
                "formula": row["formula"] or "",
                "smiles": row["smiles"] or "",
                "inchi": row["inchi"] or "",
                "mass": row["mass"],
                "volume": row["volume"],
                "type": row["type"] or "",
                "tags": tags,
                "charge": row["charge"],
                "spin": row["spin"],
                "atoms": atoms,
                "bonds": bonds,
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


# ========== 分子详情接口 ==========

@router.get("/molecule/detail/{molecule_id}")
async def get_molecule_detail(molecule_id: int):
    """
    获取分子详情
    - molecule_id: 分子ID
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, formula, smiles, inchi, mass, volume, type, tags, charge, spin, atoms, bonds, createTime
            FROM molecules
            WHERE id = ?
            """,
            (molecule_id,)
        )
        row = cursor.fetchone()

        if not row:
            return {
                "code": 404,
                "msg": "分子不存在",
                "data": None
            }

        # 解析 JSON 字符串
        tags = []
        atoms = []
        bonds = []

        try:
            if row["tags"]:
                tags = json.loads(row["tags"])
        except (json.JSONDecodeError, TypeError):
            pass

        try:
            if row["atoms"]:
                atoms = json.loads(row["atoms"])
        except (json.JSONDecodeError, TypeError):
            pass

        try:
            if row["bonds"]:
                bonds = json.loads(row["bonds"])
        except (json.JSONDecodeError, TypeError):
            pass

        return {
            "code": 200,
            "msg": None,
            "data": {
                "id": row["id"],
                "formula": row["formula"] or "",
                "smiles": row["smiles"] or "",
                "inchi": row["inchi"] or "",
                "mass": row["mass"],
                "volume": row["volume"],
                "type": row["type"] or "",
                "tags": tags,
                "charge": row["charge"],
                "spin": row["spin"],
                "atoms": atoms,
                "bonds": bonds,
                "createTime": row["createTime"] or ""
            }
        }


# ========== 分子标签列表接口 ==========

@router.get("/molecule/tags")
async def get_molecule_tags():
    """
    获取分子标签列表
    """
    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, count, category FROM molecule_tags ORDER BY count DESC, name"
        )
        rows = cursor.fetchall()

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


# ========== 分子相似性搜索接口 ==========

@router.post("/molecule/similarity")
async def molecule_similarity_search(request: SimilarityRequest):
    """
    分子相似性搜索
    - smiles: 查询分子的 SMILES 字符串
    - type: 搜索类型，默认为 "2d"
    - threshold: 相似度阈值，默认为 0.7

    注：由于 SQLite 不支持化学指纹和相似性计算，
    这里使用简化实现：通过子字符串匹配或基于分子量相近来模拟相似性
    """
    from rdkit import Chem
    from rdkit import DataStructs
    from rdkit.Chem import AllChem

    query_smiles = request.smiles
    search_type = request.type or "2d"
    threshold = request.threshold if request.threshold is not None else 0.7

    try:
        # 解析查询分子的 SMILES
        query_mol = Chem.MolFromSmiles(query_smiles)
        if not query_mol:
            return {
                "code": 400,
                "msg": "无效的 SMILES 字符串",
                "data": None
            }

        # 生成查询分子的指纹
        if search_type == "2d":
            query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, 2, nBits=2048)
        else:
            query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, 3, nBits=2048)

    except Exception as e:
        return {
            "code": 400,
            "msg": f"SMILES 解析失败: {str(e)}",
            "data": None
        }

    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 获取所有有 SMILES 的分子
        cursor.execute(
            """
            SELECT id, formula, smiles, inchi, mass, volume, type, tags, charge, spin, atoms, bonds, createTime
            FROM molecules
            WHERE smiles IS NOT NULL AND smiles != ''
            """
        )
        rows = cursor.fetchall()

        # 计算相似度
        similar_molecules = []

        for row in rows:
            smiles = row["smiles"]
            if not smiles:
                continue

            try:
                mol = Chem.MolFromSmiles(smiles)
                if not mol:
                    continue

                # 生成分子指纹
                if search_type == "2d":
                    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
                else:
                    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 3, nBits=2048)

                # 计算 Tanimoto 相似度
                similarity = DataStructs.TanimotoSimilarity(query_fp, fp)

                # 只保留相似度大于等于阈值的分子
                if similarity >= threshold:
                    # 解析 JSON 字符串
                    tags = []
                    atoms = []
                    bonds = []

                    try:
                        if row["tags"]:
                            tags = json.loads(row["tags"])
                    except (json.JSONDecodeError, TypeError):
                        pass

                    try:
                        if row["atoms"]:
                            atoms = json.loads(row["atoms"])
                    except (json.JSONDecodeError, TypeError):
                        pass

                    try:
                        if row["bonds"]:
                            bonds = json.loads(row["bonds"])
                    except (json.JSONDecodeError, TypeError):
                        pass

                    similar_molecules.append({
                        "id": row["id"],
                        "formula": row["formula"] or "",
                        "smiles": row["smiles"] or "",
                        "inchi": row["inchi"] or "",
                        "mass": row["mass"],
                        "volume": row["volume"],
                        "type": row["type"] or "",
                        "tags": tags,
                        "charge": row["charge"],
                        "spin": row["spin"],
                        "atoms": atoms,
                        "bonds": bonds,
                        "createTime": row["createTime"] or "",
                        "similarity": round(similarity, 4)
                    })

            except Exception:
                continue

        # 按相似度降序排序
        similar_molecules.sort(key=lambda x: x["similarity"], reverse=True)

        return {
            "code": 200,
            "msg": None,
            "data": {
                "result": similar_molecules
            }
        }
