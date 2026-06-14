import sqlite3
import json

def init_db(db_path='molecules.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # 构建 DDL。
        # 包含一个自增 ID 作为主键，其余字段根据 JSON key 动态映射类型。
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS molecules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inchikey TEXT UNIQUE,
                atomstereoCount INTEGER,
                smiles TEXT,
                bondStereoCount INTEGER,
                categoryObject TEXT,
                canonicalInchikey TEXT,
                categoryLabel TEXT,
                definedBondStereoCount INTEGER,
                featureanionCount3d INTEGER,
                featuredonorCount3d INTEGER,
                isotopeAtomCount INTEGER,
                featurecationCount3d INTEGER,
                canonicalInchi TEXT,
                publicIdentification INTEGER,
                iupac TEXT,
                sourceResearchGroup TEXT,
                picId TEXT,
                inchi TEXT,
                author TEXT,
                volume3d REAL,
                canonicalSmiles TEXT,
                weight REAL,
                conformerCount3d INTEGER,
                monoisotopicMass REAL,
                undefinedBondStereoCount INTEGER,
                displayFormula TEXT,
                redundantFields2 TEXT,
                redundantFields3 TEXT,
                covalentUnitCount INTEGER,
                featureringCount3d INTEGER,
                redundantFields1 TEXT,
                featureCount3d INTEGER,
                definedAtomStereoCount INTEGER,
                cid INTEGER,
                complexity REAL,
                accountName TEXT,
                referenceCitation TEXT,
                delFlag INTEGER,
                title TEXT,
                undefinedAtomStereoCount INTEGER,
                exactMass REAL,
                cas TEXT,
                xstericquadrupole3d REAL,
                sourcePath TEXT,
                conformermodelrmsd3d REAL,
                featurehydrophobeCount3d INTEGER,
                collectTime INTEGER,
                hbondDonorCount INTEGER,
                uniqueIdentification TEXT,
                molecularName TEXT,
                charge INTEGER,
                effectiverotorCount3d INTEGER,
                xlogp REAL,
                hbondAcceptorCount INTEGER,
                heavyAtomCount INTEGER,
                ystericquadrupole3d REAL,
                zstericquadrupole3d REAL,
                formula TEXT,
                featureacceptorCount3d INTEGER,
                rotatableBondCount INTEGER,
                tpsa REAL
            )
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

if __name__ == '__main__':
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
    
    db_file = 'chemistry.db'
    
    # 1. 初始化表
    init_db(db_file)
    
    # 2. 插入数据
    insert_molecule(db_file, payload)
    
    print("数据库初始化并写入成功。")