"""
测试信息抽取模块
"""
import unittest
from app.services.extractor import extract_entities


class TestExtractor(unittest.TestCase):
    """
    测试信息抽取模块
    """
    
    def test_extract_entities(self):
        """
        测试抽取实体
        """
        # 测试文档
        test_doc = {
            "doc_id": "test_doc",
            "paragraphs": [
                "合同金额为¥100000.00元",
                "签订日期为2024年12月1日",
                "联系电话为13812345678",
                "邮箱为test@example.com",
                "增长率为15.5%"
            ],
            "tables": [],
            "raw_text": "合同金额为¥100000.00元 签订日期为2024年12月1日 联系电话为13812345678 邮箱为test@example.com 增长率为15.5%"
        }
        
        # 提取实体
        entities = extract_entities(test_doc)
        
        # 验证结果
        self.assertIsInstance(entities, list)
        
        # 检查是否提取到了所有类型的实体
        entity_types = [ent['entity_type'] for ent in entities]
        self.assertIn("金额", entity_types)
        self.assertIn("日期", entity_types)
        self.assertIn("电话", entity_types)
        self.assertIn("邮箱", entity_types)
        self.assertIn("百分比", entity_types)
        
        # 检查实体值
        entity_values = [ent['value'] for ent in entities]
        self.assertIn("¥100000.00", entity_values)
        self.assertIn("2024年12月1日", entity_values)
        self.assertIn("13812345678", entity_values)
        self.assertIn("test@example.com", entity_values)
        self.assertIn("15.5%", entity_values)
    
    def test_extract_entities_empty(self):
        """
        测试抽取空文档
        """
        # 空文档
        test_doc = {
            "doc_id": "test_doc",
            "paragraphs": [],
            "tables": [],
            "raw_text": ""
        }
        
        # 提取实体
        entities = extract_entities(test_doc)
        
        # 验证结果
        self.assertIsInstance(entities, list)
        self.assertEqual(len(entities), 0)
    
    def test_extract_entities_with_tables(self):
        """
        测试从表格中抽取实体
        """
        # 带表格的文档
        test_doc = {
            "doc_id": "test_doc",
            "paragraphs": [],
            "tables": [
                [
                    ["名称", "金额", "日期"],
                    ["项目1", "¥50000", "2024-01-01"],
                    ["项目2", "¥30000", "2024-02-01"]
                ]
            ],
            "raw_text": "名称 金额 日期 项目1 ¥50000 2024-01-01 项目2 ¥30000 2024-02-01"
        }
        
        # 提取实体
        entities = extract_entities(test_doc)
        
        # 验证结果
        self.assertIsInstance(entities, list)
        
        # 检查是否提取到了表格中的实体
        entity_values = [ent['value'] for ent in entities]
        self.assertIn("¥50000", entity_values)
        self.assertIn("¥30000", entity_values)
        self.assertIn("2024-01-01", entity_values)
        self.assertIn("2024-02-01", entity_values)


if __name__ == '__main__':
    unittest.main()
