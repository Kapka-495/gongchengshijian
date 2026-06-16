"""
RAG (Retrieval-Augmented Generation) 检索模块
从向量数据库中检索与问题相关的知识
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional

import tomli
import chromadb
from chromadb.config import Settings


# ========== 配置加载 ==========
def load_rag_config():
    """从 config.toml 加载配置"""
    config_file = Path(__file__).resolve().parent.parent / "config" / "config.toml"
    if config_file.exists():
        with open(config_file, "rb") as f:
            return tomli.load(f)
    return {}


_config = load_rag_config()
_db_config = _config.get("database", {})
_rag_config = _config.get("rag", {})

# 数据库路径（优先使用配置，否则使用默认）
DB_PATH = Path(__file__).resolve().parent.parent / _db_config.get("path", "db_table/") / "chemistry.db"
CHROMA_PATH = Path(__file__).resolve().parent.parent / _rag_config.get("chroma_path", "db_table/chroma_db")

# 全局 Chroma 客户端（单例）
_chroma_client = None
_collection = None


def get_db_path():
    """获取数据库路径"""
    return str(DB_PATH)


def get_chroma_client():
    """获取 Chroma 客户端（单例）"""
    global _chroma_client
    if _chroma_client is None:
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return _chroma_client


def get_collection():
    """获取知识库集合"""
    global _collection
    if _collection is None:
        client = get_chroma_client()
        try:
            _collection = client.get_collection("chemistry_knowledge")
        except Exception:
            # 集合不存在则创建
            _collection = client.create_collection(
                name="chemistry_knowledge",
                metadata={"description": "化学知识库"}
            )
    return _collection


def init_knowledge_base():
    """
    初始化知识库
    从 SQLite 数据库读取分子、材料、文献数据，构建可检索的知识条目
    """
    collection = get_collection()

    # 检查是否已有数据
    if collection.count() > 0:
        print(f"知识库已有 {collection.count()} 条记录，跳过初始化")
        return

    knowledge_items = []

    # 1. 从分子表读取
    try:
        with sqlite3.connect(get_db_path()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM molecules LIMIT 1000")
            for row in cursor.fetchall():
                row_dict = dict(row)
                # 构造知识文本
                text = format_molecule_knowledge(row_dict)
                if text:
                    knowledge_items.append({
                        "text": text,
                        "source": "molecule",
                        "source_id": row_dict.get("id")
                    })
    except Exception as e:
        print(f"读取分子数据失败: {e}")

    # 2. 从材料表读取
    try:
        with sqlite3.connect(get_db_path()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM materials LIMIT 500")
            for row in cursor.fetchall():
                row_dict = dict(row)
                text = format_material_knowledge(row_dict)
                if text:
                    knowledge_items.append({
                        "text": text,
                        "source": "material",
                        "source_id": row_dict.get("id")
                    })
    except Exception as e:
        print(f"读取材料数据失败: {e}")

    # 3. 从文献表读取
    try:
        with sqlite3.connect(get_db_path()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM literature LIMIT 500")
            for row in cursor.fetchall():
                row_dict = dict(row)
                text = format_literature_knowledge(row_dict)
                if text:
                    knowledge_items.append({
                        "text": text,
                        "source": "literature",
                        "source_id": row_dict.get("id")
                    })
    except Exception as e:
        print(f"读取文献数据失败: {e}")

    # 添加到 Chroma
    if knowledge_items:
        texts = [item["text"] for item in knowledge_items]
        ids = [f"{item['source']}_{item['source_id']}" for item in knowledge_items]
        metadatas = [
            {"source": item["source"], "source_id": item["source_id"]}
            for item in knowledge_items
        ]

        collection.add(documents=texts, ids=ids, metadatas=metadatas)
        print(f"知识库初始化完成，共添加 {len(knowledge_items)} 条记录")


def format_molecule_knowledge(row: Dict[str, Any]) -> str:
    """将分子数据格式化为知识文本"""
    parts = []

    if row.get("formula"):
        parts.append(f"化学式：{row['formula']}")
    if row.get("smiles"):
        parts.append(f"SMILES：{row['smiles']}")
    if row.get("inchi"):
        parts.append(f"InChI：{row['inchi']}")
    if row.get("mass"):
        parts.append(f"分子量：{row['mass']}")
    if row.get("charge") is not None:
        parts.append(f"电荷：{row['charge']}")
    if row.get("type"):
        parts.append(f"类型：{row['type']}")
    if row.get("tags"):
        tags = row["tags"]
        if isinstance(tags, str):
            parts.append(f"标签：{tags}")
        else:
            parts.append(f"标签：{', '.join(tags)}")

    if not parts:
        return ""

    return "分子信息：" + "；".join(parts)


def format_material_knowledge(row: Dict[str, Any]) -> str:
    """将材料数据格式化为知识文本"""
    parts = []

    if row.get("name"):
        parts.append(f"材料名称：{row['name']}")
    if row.get("formula"):
        parts.append(f"化学式：{row['formula']}")
    if row.get("type"):
        parts.append(f"类型：{row['type']}")
    if row.get("band_gap"):
        parts.append(f"带隙：{row['band_gap']} eV")
    if row.get("crystal_system"):
        parts.append(f"晶体系统：{row['crystal_system']}")
    if row.get("space_group"):
        parts.append(f"空间群：{row['space_group']}")
    if row.get("lattice_constant"):
        parts.append(f"晶格常数：{row['lattice_constant']}")
    if row.get("tags"):
        tags = row["tags"]
        if isinstance(tags, str):
            parts.append(f"标签：{tags}")
        else:
            parts.append(f"标签：{', '.join(tags)}")

    if not parts:
        return ""

    return "材料信息：" + "；".join(parts)


def format_literature_knowledge(row: Dict[str, Any]) -> str:
    """将文献数据格式化为知识文本"""
    parts = []

    if row.get("title"):
        parts.append(f"标题：{row['title']}")
    if row.get("authors"):
        authors = row["authors"]
        if isinstance(authors, str):
            parts.append(f"作者：{authors}")
        else:
            parts.append(f"作者：{', '.join(authors)}")
    if row.get("journal"):
        parts.append(f"期刊：{row['journal']}")
    if row.get("year"):
        parts.append(f"发表年份：{row['year']}")
    if row.get("doi"):
        parts.append(f"DOI：{row['doi']}")
    if row.get("abstract"):
        parts.append(f"摘要：{row['abstract']}")
    if row.get("keywords"):
        parts.append(f"关键词：{row['keywords']}")

    if not parts:
        return ""

    return "文献信息：" + "；".join(parts)


def retrieve(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    检索与问题最相关的知识

    Args:
        query: 用户问题
        top_k: 返回的最相关条目数量

    Returns:
        相关知识列表
    """
    collection = get_collection()

    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        retrieved = []
        if results and results.get("documents"):
            doc_list = results["documents"][0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]

            for i, doc in enumerate(doc_list):
                retrieved.append({
                    "text": doc,
                    "source": metadatas[i].get("source") if i < len(metadatas) else "unknown",
                    "source_id": metadatas[i].get("source_id") if i < len(metadatas) else None,
                    "relevance": 1 - distances[i] if i < len(distances) else 0
                })

        return retrieved

    except Exception as e:
        print(f"检索失败: {e}")
        return []


def format_retrieved_context(retrieved: List[Dict[str, Any]]) -> str:
    """将检索结果格式化为上下文字符串"""
    if not retrieved:
        return "（知识库中未找到相关信息）"

    contexts = []
    for i, item in enumerate(retrieved, 1):
        contexts.append(f"{i}. {item['text']}")

    return "\n".join(contexts)


# 测试用
if __name__ == "__main__":
    init_knowledge_base()
    results = retrieve("水的化学式是什么")
    print("检索结果：")
    for r in results:
        print(f"- {r['text']}")