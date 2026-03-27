"""
知识池模块
管理文档和实体的存储与查询
"""
import sqlite3
import json
from typing import List, Dict, Any
from datetime import datetime
from ..database import get_db_connection


class KnowledgePool:
    """
    知识池类，管理文档和实体的存储与查询
    """
    
    def __init__(self):
        """
        初始化知识池
        """
        self._init_database()
    
    def _init_database(self):
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
    
    def save_document(self, doc_id: str, parsed_doc: Dict[str, Any], entities: List[Dict[str, Any]]):
        """
        保存文档和实体到数据库
        
        Args:
            doc_id: 文档 ID
            parsed_doc: 解析后的文档
            entities: 抽取的实体列表
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # 保存文档
            parsed_content = json.dumps(parsed_doc)
            create_time = datetime.now().isoformat()
            
            cursor.execute(
                "INSERT OR REPLACE INTO documents (doc_id, parsed_content, create_time) VALUES (?, ?, ?)",
                (doc_id, parsed_content, create_time)
            )
            
            # 保存实体
            for entity in entities:
                cursor.execute(
                    "INSERT INTO entities (doc_id, entity_type, value, paragraph_index, confidence) VALUES (?, ?, ?, ?, ?)",
                    (
                        doc_id,
                        entity['entity_type'],
                        entity['value'],
                        entity['paragraph_index'],
                        entity['confidence']
                    )
                )
            
            conn.commit()
        except Exception as e:
            print(f"保存文档时出错: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_entities_by_doc_id(self, doc_id: str) -> List[Dict[str, Any]]:
        """
        根据文档 ID 获取实体
        
        Args:
            doc_id: 文档 ID
        
        Returns:
            实体列表
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT entity_type, value, paragraph_index, confidence FROM entities WHERE doc_id = ?",
                (doc_id,)
            )
            
            entities = []
            for row in cursor.fetchall():
                entities.append({
                    "entity_type": row[0],
                    "value": row[1],
                    "paragraph_index": row[2],
                    "confidence": row[3]
                })
            
            return entities
        except Exception as e:
            print(f"获取实体时出错: {e}")
            return []
        finally:
            conn.close()
    
    def get_all_entities(self) -> List[Dict[str, Any]]:
        """
        获取所有实体
        
        Returns:
            实体列表
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT doc_id, entity_type, value, paragraph_index, confidence FROM entities"
            )
            
            entities = []
            for row in cursor.fetchall():
                entities.append({
                    "entity_type": row[1],
                    "value": row[2],
                    "source_doc": row[0],
                    "paragraph_index": row[3],
                    "confidence": row[4]
                })
            
            return entities
        except Exception as e:
            print(f"获取所有实体时出错: {e}")
            return []
        finally:
            conn.close()
    
    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """
        根据文档 ID 获取文档
        
        Args:
            doc_id: 文档 ID
        
        Returns:
            文档信息
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT parsed_content, create_time FROM documents WHERE doc_id = ?",
                (doc_id,)
            )
            
            row = cursor.fetchone()
            if row:
                return {
                    "doc_id": doc_id,
                    "parsed_content": json.loads(row[0]),
                    "create_time": row[1]
                }
            return None
        except Exception as e:
            print(f"获取文档时出错: {e}")
            return None
        finally:
            conn.close()
    
    def delete_document(self, doc_id: str):
        """
        删除文档及其关联的实体
        
        Args:
            doc_id: 文档 ID
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # 删除关联的实体
            cursor.execute("DELETE FROM entities WHERE doc_id = ?", (doc_id,))
            
            # 删除文档
            cursor.execute("DELETE FROM documents WHERE doc_id = ?", (doc_id,))
            
            conn.commit()
        except Exception as e:
            print(f"删除文档时出错: {e}")
            conn.rollback()
        finally:
            conn.close()