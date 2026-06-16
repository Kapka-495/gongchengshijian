"""
用于建立数据库的表,建表时只运行一次即可

"""

import sqlite3
import tomli
import os
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
os.chdir(parent_dir)

def init_db(db_path='chemistry.db'):
    # init_molecules_table(db_path)
    init_users_table(db_path)
    init_visitor_count_table(db_path)
    init_news_table(db_path)
    init_announcements_table(db_path)
    init_molecules_table(db_path)
    init_materials_table(db_path)
    init_literature_table(db_path)
    init_molecule_tags_table(db_path)
    init_material_tags_table(db_path)
    init_audit_logs_table(db_path)
    init_metadata_table(db_path)
    init_spectrum_table(db_path)
    init_category_summary_table(db_path)
    init_molecule_summary_table(db_path)
    init_obs_files_table(db_path)
    init_spectrum_types_table(db_path)

    


# def init_molecules_table(db_path='chemistry.db'):
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
        
#         # 构建 DDL。
#         # 包含一个自增 ID 作为主键，其余字段根据 JSON key 动态映射类型。
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS molecules (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 inchikey TEXT UNIQUE,
#                 atomstereoCount INTEGER,
#                 smiles TEXT,
#                 bondStereoCount INTEGER,
#                 categoryObject TEXT,
#                 canonicalInchikey TEXT,
#                 categoryLabel TEXT,
#                 definedBondStereoCount INTEGER,
#                 featureanionCount3d INTEGER,
#                 featuredonorCount3d INTEGER,
#                 isotopeAtomCount INTEGER,
#                 featurecationCount3d INTEGER,
#                 canonicalInchi TEXT,
#                 publicIdentification INTEGER,
#                 iupac TEXT,
#                 sourceResearchGroup TEXT,
#                 picId TEXT,
#                 inchi TEXT,
#                 author TEXT,
#                 volume3d REAL,
#                 canonicalSmiles TEXT,
#                 weight REAL,
#                 conformerCount3d INTEGER,
#                 monoisotopicMass REAL,
#                 undefinedBondStereoCount INTEGER,
#                 displayFormula TEXT,
#                 redundantFields2 TEXT,
#                 redundantFields3 TEXT,
#                 covalentUnitCount INTEGER,
#                 featureringCount3d INTEGER,
#                 redundantFields1 TEXT,
#                 featureCount3d INTEGER,
#                 definedAtomStereoCount INTEGER,
#                 cid INTEGER,
#                 complexity REAL,
#                 accountName TEXT,
#                 referenceCitation TEXT,
#                 delFlag INTEGER,
#                 title TEXT,
#                 undefinedAtomStereoCount INTEGER,
#                 exactMass REAL,
#                 cas TEXT,
#                 xstericquadrupole3d REAL,
#                 sourcePath TEXT,
#                 conformermodelrmsd3d REAL,
#                 featurehydrophobeCount3d INTEGER,
#                 collectTime INTEGER,
#                 hbondDonorCount INTEGER,
#                 uniqueIdentification TEXT,
#                 molecularName TEXT,
#                 charge INTEGER,
#                 effectiverotorCount3d INTEGER,
#                 xlogp REAL,
#                 hbondAcceptorCount INTEGER,
#                 heavyAtomCount INTEGER,
#                 ystericquadrupole3d REAL,
#                 zstericquadrupole3d REAL,
#                 formula TEXT,
#                 featureacceptorCount3d INTEGER,
#                 rotatableBondCount INTEGER,
#                 tpsa REAL
#             )
#         ''')
#         conn.commit()

def init_users_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # 构建 DDL
        # 包含自增 ID 作为主键，其余字段根据提供的接口数据动态映射
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                role TEXT,
                nickname TEXT,
                phone TEXT,
                avatar TEXT,
                createTime TEXT
            )
        ''')
        conn.commit()

def init_visitor_count_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visitor_count (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                count INTEGER NOT NULL DEFAULT 0
            )
        ''')

        # 初始化访客计数为随机值（如果还没有记录）
        cursor.execute('''
            INSERT OR IGNORE INTO visitor_count (id, count)
            VALUES (1, ABS(RANDOM()) % 50000 + 10000)
        ''')
        conn.commit()

def init_news_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                author TEXT,
                summary TEXT,
                createTime TEXT
            )
        ''')
        conn.commit()

def init_announcements_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                author TEXT,
                importance TEXT,
                createTime TEXT
            )
        ''')
        conn.commit()

def init_molecules_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # 注意：SQLite 没有原生数组/JSON类型，tags, atoms, bonds 存为 TEXT (存入时需 json.dumps)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS molecules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                picId TEXT UNIQUE,
                inchikey TEXT,
                canonicalInchikey TEXT,
                smiles TEXT,
                canonicalSmiles TEXT,
                inchi TEXT,
                canonicalInchi TEXT,
                iupac TEXT,
                molecularName TEXT,
                title TEXT,
                displayFormula TEXT,
                formula TEXT,
                exactMass REAL,
                monoisotopicMass REAL,
                weight REAL,
                mass REAL,
                categoryLabel TEXT,
                categoryObject TEXT,
                type TEXT,
                tags TEXT,
                charge INTEGER,
                spin INTEGER,
                author TEXT,
                sourceResearchGroup TEXT,
                accountName TEXT,
                cas TEXT,
                cid INTEGER,
                volume REAL,
                volume3d REAL,
                xlogp REAL,
                complexity REAL,
                tpsa REAL,
                hbondDonorCount INTEGER,
                hbondAcceptorCount INTEGER,
                rotatableBondCount INTEGER,
                heavyAtomCount INTEGER,
                isotopeAtomCount INTEGER,
                definedAtomStereoCount INTEGER,
                undefinedAtomStereoCount INTEGER,
                definedBondStereoCount INTEGER,
                undefinedBondStereoCount INTEGER,
                atomstereoCount INTEGER,
                bondStereoCount INTEGER,
                covalentUnitCount INTEGER,
                featureCount3d INTEGER,
                featureacceptorCount3d INTEGER,
                featuredonorCount3d INTEGER,
                featurecationCount3d INTEGER,
                featureanionCount3d INTEGER,
                featurehydrophobeCount3d INTEGER,
                featureringCount3d INTEGER,
                effectiverotorCount3d INTEGER,
                conformerCount3d INTEGER,
                conformermodelrmsd3d REAL,
                xstericquadrupole3d REAL,
                ystericquadrupole3d REAL,
                zstericquadrupole3d REAL,
                publicIdentification INTEGER,
                uniqueIdentification TEXT,
                referenceCitation TEXT,
                sourcePath TEXT,
                delFlag INTEGER,
                collectTime INTEGER,
                atoms TEXT,
                bonds TEXT,
                createTime TEXT
            )
        ''')
        conn.commit()

def init_materials_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                formula TEXT,
                type TEXT,
                tags TEXT,
                bandGap REAL,
                latticeConstant REAL,
                crystalSystem TEXT,
                spaceGroup TEXT,
                createTime TEXT
            )
        ''')
        conn.commit()

def init_literature_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS literature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doi TEXT UNIQUE,
                title TEXT NOT NULL,
                authors TEXT,
                journal TEXT,
                year INTEGER,
                volume TEXT,
                issue TEXT,
                pages TEXT,
                abstract TEXT,
                keywords TEXT,
                tags TEXT
            )
        ''')
        conn.commit()

def init_molecule_tags_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS molecule_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                count INTEGER DEFAULT 0,
                category TEXT
            )
        ''')
        conn.commit()

def init_material_tags_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS material_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                count INTEGER DEFAULT 0,
                category TEXT
            )
        ''')
        conn.commit()

def get_visitor_count(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT count FROM visitor_count WHERE id = 1')
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0

def increment_visitor_count(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE visitor_count SET count = count + 1 WHERE id = 1
        ''')
        conn.commit()


def insert_molecule(db_path, mol_data):
    """
    动态生成 SQL 语句并插入单条分子数据。
    使用参数化查询防御注入，Python 的 None 会自动被 sqlite3 转换为 SQL 的 NULL。
    """
    keys = list(mol_data.keys())
    values = tuple(mol_data[k] for k in keys)
    
    columns = ','.join(keys)
    placeholders = ','.join(['?'] * len(keys))
    
    # 若 inchikey 冲突则替换更新
    sql = f'''
        INSERT OR REPLACE INTO molecules ({columns})
        VALUES ({placeholders})
    '''
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()


def init_audit_logs_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER NOT NULL,
                username TEXT NOT NULL,
                action TEXT,
                resource TEXT,
                detail TEXT,
                ip TEXT,
                time TEXT
            )
        ''')
        conn.commit()

def init_metadata_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # required 字段在 SQLite 中用 INTEGER (0 或 1) 表示布尔值
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fieldEn TEXT UNIQUE NOT NULL,
                fieldZh TEXT,
                type TEXT,
                required INTEGER DEFAULT 0,
                description TEXT
            )
        ''')
        conn.commit()

def init_spectrum_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # 展平嵌套结构：每条光谱数据独立成行，通过 picId 关联 molecule。
        # peaks 和 dataPoints 数组存为 TEXT（入库时 json.dumps）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spectrum (
                id TEXT PRIMARY KEY,
                picId INTEGER NOT NULL,
                type TEXT,
                name TEXT,
                instrument TEXT,
                conditions TEXT,
                xLabel TEXT,
                yLabel TEXT,
                peaks TEXT,
                dataPoints TEXT
            )
        ''')
        conn.commit()

def init_category_summary_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT UNIQUE NOT NULL,
                count INTEGER DEFAULT 0,
                percentage REAL
            )
        ''')
        conn.commit()

def init_molecule_summary_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS molecule_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                updateTime TEXT
            )
        ''')
        conn.commit()

def init_obs_files_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # 注意此处的 id 格式为 'obs-xxx'，直接使用 TEXT 作为主键
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS obs_files (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                size INTEGER,
                type TEXT,
                uploadTime TEXT,
                moleculeId INTEGER,
                description TEXT
            )
        ''')
        conn.commit()

def init_spectrum_types_table(db_path='chemistry.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spectrum_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT UNIQUE NOT NULL,
                label TEXT,
                count INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

if __name__ == '__main__':
    with open("config\config.toml", "rb") as f:
        config = tomli.load(f)
    db_path = config["database"]["path"]
    # 你的源 JSON 数据
    payload = {
        "inchikey": "VXKWYPOMXBVZSJ-UHFFFAOYSA-N",
        "atomstereoCount": 0,
        "smiles": "C[Sn](C)(C)C",
        "bondStereoCount": 0,
        "categoryObject": "molecule",
        "canonicalInchikey": "VXKWYPOMXBVZSJ-UHFFFAOYSA-N",
        "categoryLabel": "Open database",
        "definedBondStereoCount": 0,
        "featureanionCount3d": 0,
        "featuredonorCount3d": 0,
        "isotopeAtomCount": 0,
        "featurecationCount3d": 0,
        "canonicalInchi": "1S/4CH3.Sn/h4*1H3;",
        "publicIdentification": 1,
        "iupac": "tetramethylstannane",
        "sourceResearchGroup": "1-5",
        "picId": "picd-mol-11661",
        "inchi": "1S/4CH3.Sn/h4*1H3;",
        "author": "linjiangchen",
        "volume3d": None,
        "canonicalSmiles": "C[Sn](C)(C)C",
        "weight": 178.85,
        "conformerCount3d": 0,
        "monoisotopicMass": 179.996103,
        "undefinedBondStereoCount": 0,
        "displayFormula": "C4H12Sn",
        "redundantFields2": None,
        "redundantFields3": None,
        "covalentUnitCount": 1,
        "featureringCount3d": 0,
        "redundantFields1": None,
        "featureCount3d": 0,
        "definedAtomStereoCount": 0,
        "cid": 11661,
        "complexity": 19.0,
        "accountName": "chenlinjiang_1-5",
        "referenceCitation": None,
        "delFlag": 1,
        "title": "Tetramethyltin",
        "undefinedAtomStereoCount": 0,
        "exactMass": 179.996103,
        "cas": None,
        "xstericquadrupole3d": None,
        "sourcePath": "clickhouse",
        "conformermodelrmsd3d": None,
        "featurehydrophobeCount3d": 0,
        "collectTime": 1760645233000,
        "hbondDonorCount": 0,
        "uniqueIdentification": "7940b039174ca5dba01d92a0afcb3619",
        "molecularName": None,
        "charge": 0,
        "effectiverotorCount3d": 0,
        "xlogp": None,
        "hbondAcceptorCount": 0,
        "heavyAtomCount": 5,
        "ystericquadrupole3d": None,
        "zstericquadrupole3d": None,
        "formula": "C4H12Sn",
        "featureacceptorCount3d": 0,
        "rotatableBondCount": 0,
        "tpsa": 0.0
    }
    
    db_path = db_path + 'chemistry.db'
    
    # 1. 初始化表
    init_db(db_path)
    
    # 2. 插入数据
    # insert_molecule(db_path, payload)
    
    print("数据库初始化成功。")