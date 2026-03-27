"""
数据库模块
封装 SQLite 数据库连接、表创建与基础 CRUD 操作
"""
import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_pool.db')


def get_db_connection():
    """
    获取数据库连接
    
    Returns:
        sqlite3.Connection: 数据库连接
    """
    # 确保数据目录存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # 创建连接
    conn = sqlite3.connect(DB_PATH)
    
    # 设置行工厂，使查询结果返回字典形式
    conn.row_factory = sqlite3.Row
    
    return conn


def init_database():
    """
    初始化数据库表结构
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建文档表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        parsed_content TEXT,
        create_time TIMESTAMP
    )
    ''')
    
    # 创建实体表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id TEXT,
        entity_type TEXT,
        value TEXT,
        paragraph_index INTEGER,
        confidence REAL,
        FOREIGN KEY (doc_id) REFERENCES documents (doc_id)
    )
    ''')
    
    conn.commit()
    conn.close()