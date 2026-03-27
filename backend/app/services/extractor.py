"""
信息抽取模块
支持规则（正则表达式）、NER 模型和大语言模型的信息抽取
"""
import re
import json
from typing import List, Dict, Any

# 正则表达式模式
AMOUNT_PATTERN = r'[¥￥$\$]?\s*\d+(?:\.\d{1,2})?'
DATE_PATTERN = r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?'
PERCENTAGE_PATTERN = r'\d+(?:\.\d{1,2})?%'
PHONE_PATTERN = r'1[3-9]\d{9}'
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# 加载 spaCy 模型（如果可用）
nlp = None
try:
    import spacy
    nlp = spacy.load('zh_core_web_sm')
except Exception:
    pass


def extract_entities(parsed_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    从解析后的文档中抽取实体
    
    Args:
        parsed_doc: 解析后的文档结构
    
    Returns:
        实体列表
    """
    entities = []
    
    # 从段落中抽取实体
    for i, paragraph in enumerate(parsed_doc.get('paragraphs', [])):
        # 使用正则表达式抽取
        regex_entities = _extract_with_regex(paragraph, i, parsed_doc.get('doc_id', ''))
        entities.extend(regex_entities)
        
        # 使用 NER 模型抽取（如果可用）
        if nlp:
            ner_entities = _extract_with_ner(paragraph, i, parsed_doc.get('doc_id', ''))
            entities.extend(ner_entities)
    
    # 从表格中抽取实体
    for table in parsed_doc.get('tables', []):
        for row in table:
            for cell in row:
                if cell:
                    # 使用正则表达式抽取表格中的实体
                    table_entities = _extract_with_regex(cell, 0, parsed_doc.get('doc_id', ''))
                    entities.extend(table_entities)
    
    # 去重
    entities = _deduplicate_entities(entities)
    
    return entities


def _extract_with_regex(text: str, paragraph_index: int, source_doc: str) -> List[Dict[str, Any]]:
    """
    使用正则表达式抽取实体
    """
    entities = []
    
    # 抽取金额
    for match in re.finditer(AMOUNT_PATTERN, text):
        entities.append({
            "entity_type": "金额",
            "value": match.group().strip(),
            "source_doc": source_doc,
            "paragraph_index": paragraph_index,
            "confidence": 0.9
        })
    
    # 抽取日期
    for match in re.finditer(DATE_PATTERN, text):
        entities.append({
            "entity_type": "日期",
            "value": match.group().strip(),
            "source_doc": source_doc,
            "paragraph_index": paragraph_index,
            "confidence": 0.9
        })
    
    # 抽取百分比
    for match in re.finditer(PERCENTAGE_PATTERN, text):
        entities.append({
            "entity_type": "百分比",
            "value": match.group().strip(),
            "source_doc": source_doc,
            "paragraph_index": paragraph_index,
            "confidence": 0.9
        })
    
    # 抽取电话
    for match in re.finditer(PHONE_PATTERN, text):
        entities.append({
            "entity_type": "电话",
            "value": match.group().strip(),
            "source_doc": source_doc,
            "paragraph_index": paragraph_index,
            "confidence": 0.95
        })
    
    # 抽取邮箱
    for match in re.finditer(EMAIL_PATTERN, text):
        entities.append({
            "entity_type": "邮箱",
            "value": match.group().strip(),
            "source_doc": source_doc,
            "paragraph_index": paragraph_index,
            "confidence": 0.95
        })
    
    return entities


def _extract_with_ner(text: str, paragraph_index: int, source_doc: str) -> List[Dict[str, Any]]:
    """
    使用 NER 模型抽取实体
    """
    entities = []
    
    try:
        doc = nlp(text)
        for ent in doc.ents:
            # 映射 spaCy 实体类型到我们的实体类型
            entity_type_map = {
                'PERSON': '人物',
                'ORG': '组织',
                'GPE': '地点',
                'DATE': '日期',
                'TIME': '时间',
                'MONEY': '金额',
                'PERCENT': '百分比',
                'FAC': '设施',
                'PRODUCT': '产品',
                'EVENT': '事件',
                'WORK_OF_ART': '作品',
                'LAW': '法律',
                'LANGUAGE': '语言'
            }
            
            entity_type = entity_type_map.get(ent.label_, '其他')
            entities.append({
                "entity_type": entity_type,
                "value": ent.text.strip(),
                "source_doc": source_doc,
                "paragraph_index": paragraph_index,
                "confidence": 0.8
            })
    except Exception as e:
        print(f"NER 抽取出错: {e}")
    
    return entities


def _extract_with_llm(text: str, paragraph_index: int, source_doc: str) -> List[Dict[str, Any]]:
    """
    使用大语言模型抽取实体
    注意：这里是一个模拟实现，实际使用时需要接入真实的 LLM API
    """
    entities = []
    
    # 模拟 LLM 抽取结果
    # 实际实现时，这里应该调用 OpenAI API 或其他 LLM API
    mock_entities = [
        {"type": "项目名称", "value": "示例项目", "confidence": 0.9},
        {"type": "合同编号", "value": "HT2024001", "confidence": 0.85},
        {"type": "甲方", "value": "示例公司", "confidence": 0.8},
        {"type": "乙方", "value": "示例供应商", "confidence": 0.8}
    ]
    
    for mock_ent in mock_entities:
        entities.append({
            "entity_type": mock_ent["type"],
            "value": mock_ent["value"],
            "source_doc": source_doc,
            "paragraph_index": paragraph_index,
            "confidence": mock_ent["confidence"]
        })
    
    return entities


def _deduplicate_entities(entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    去重实体列表
    """
    seen = set()
    unique_entities = []
    
    for entity in entities:
        # 创建唯一键
        key = (entity["entity_type"], entity["value"], entity["source_doc"])
        if key not in seen:
            seen.add(key)
            unique_entities.append(entity)
    
    return unique_entities