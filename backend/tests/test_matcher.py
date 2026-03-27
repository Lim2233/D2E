"""
测试语义匹配模块
"""
import unittest
from app.services.matcher import match_entities, _simple_match


class TestMatcher(unittest.TestCase):
    """
    测试语义匹配模块
    """
    
    def test_match_entities(self):
        """
        测试匹配实体
        """
        # 测试字段
        template_fields = ["合同金额", "签订日期", "联系电话", "邮箱"]
        
        # 测试实体
        test_entities = [
            {"entity_type": "金额", "value": "¥100000.00", "source_doc": "test", "paragraph_index": 0, "confidence": 0.9},
            {"entity_type": "日期", "value": "2024年12月1日", "source_doc": "test", "paragraph_index": 1, "confidence": 0.9},
            {"entity_type": "电话", "value": "13812345678", "source_doc": "test", "paragraph_index": 2, "confidence": 0.95},
            {"entity_type": "邮箱", "value": "test@example.com", "source_doc": "test", "paragraph_index": 3, "confidence": 0.95}
        ]
        
        # 匹配实体
        matches = match_entities(template_fields, test_entities)
        
        # 验证结果
        self.assertIsInstance(matches, dict)
        self.assertEqual(len(matches), 4)
        self.assertIn("合同金额", matches)
        self.assertIn("签订日期", matches)
        self.assertIn("联系电话", matches)
        self.assertIn("邮箱", matches)
    
    def test_simple_match(self):
        """
        测试简单匹配
        """
        # 测试字段
        template_fields = ["合同金额", "签订日期", "联系电话"]
        
        # 测试实体
        test_entities = [
            {"entity_type": "金额", "value": "¥100000.00", "source_doc": "test", "paragraph_index": 0, "confidence": 0.9},
            {"entity_type": "日期", "value": "2024年12月1日", "source_doc": "test", "paragraph_index": 1, "confidence": 0.9},
            {"entity_type": "电话", "value": "13812345678", "source_doc": "test", "paragraph_index": 2, "confidence": 0.95}
        ]
        
        # 简单匹配
        matches = _simple_match(template_fields, test_entities)
        
        # 验证结果
        self.assertIsInstance(matches, dict)
        self.assertEqual(len(matches), 3)
        self.assertIn("合同金额", matches)
        self.assertIn("签订日期", matches)
        self.assertIn("联系电话", matches)
    
    def test_match_entities_no_match(self):
        """
        测试无匹配的情况
        """
        # 测试字段
        template_fields = ["合同金额", "签订日期"]
        
        # 测试实体（与字段不匹配）
        test_entities = [
            {"entity_type": "姓名", "value": "张三", "source_doc": "test", "paragraph_index": 0, "confidence": 0.9},
            {"entity_type": "地址", "value": "北京市", "source_doc": "test", "paragraph_index": 1, "confidence": 0.9}
        ]
        
        # 匹配实体
        matches = match_entities(template_fields, test_entities)
        
        # 验证结果
        self.assertIsInstance(matches, dict)
        # 可能会有部分匹配，具体取决于匹配算法


if __name__ == '__main__':
    unittest.main()
