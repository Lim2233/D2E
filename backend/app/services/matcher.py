"""
语义匹配模块
使用 sentence-transformers 计算模板字段与抽取实体的语义相似度
"""
from typing import List, Dict, Any, Tuple
import numpy as np

# 加载预训练模型
model = None
try:
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
except Exception:
    pass


def match_entities(template_fields: List[str], entities: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    将模板字段与抽取的实体进行语义匹配
    
    Args:
        template_fields: 模板字段列表
        entities: 抽取的实体列表
    
    Returns:
        字段到实体的映射
    """
    if not model:
        # 如果模型加载失败，使用简单的字符串匹配作为回退方案
        return _simple_match(template_fields, entities)
    
    # 计算字段和实体的嵌入向量
    field_embeddings = model.encode(template_fields, convert_to_tensor=True)
    
    matches = {}
    
    for i, field in enumerate(template_fields):
        # 为每个字段找到最匹配的实体
        best_match = None
        best_score = 0.0
        
        for entity in entities:
            # 计算实体类型与字段的相似度
            entity_text = f"{entity['entity_type']}: {entity['value']}"
            entity_embedding = model.encode(entity_text, convert_to_tensor=True)
            
            # 计算余弦相似度
            score = util.cos_sim(field_embeddings[i], entity_embedding).item()
            
            if score > best_score:
                best_score = score
                best_match = entity
        
        # 只保留相似度大于阈值的匹配
        if best_match and best_score > 0.5:
            matches[field] = {
                "entity": best_match,
                "score": best_score
            }
    
    return matches


def _simple_match(template_fields: List[str], entities: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    简单的字符串匹配作为回退方案
    """
    matches = {}
    
    for field in template_fields:
        best_match = None
        best_score = 0.0
        
        for entity in entities:
            # 简单的字符串包含匹配
            field_lower = field.lower()
            entity_type_lower = entity['entity_type'].lower()
            entity_value_lower = entity['value'].lower()
            
            # 计算匹配得分
            score = 0
            if entity_type_lower in field_lower:
                score += 0.7
            if entity_type_lower in entity_value_lower:
                score += 0.3
            
            if score > best_score:
                best_score = score
                best_match = entity
        
        if best_match and best_score > 0:
            matches[field] = {
                "entity": best_match,
                "score": best_score
            }
    
    return matches


def batch_match(template_fields_list: List[List[str]], entities_list: List[List[Dict[str, Any]]]) -> List[Dict[str, Dict[str, Any]]]:
    """
    批量匹配多个模板
    
    Args:
        template_fields_list: 模板字段列表的列表
        entities_list: 实体列表的列表
    
    Returns:
        每个模板的匹配结果
    """
    results = []
    
    for template_fields, entities in zip(template_fields_list, entities_list):
        result = match_entities(template_fields, entities)
        results.append(result)
    
    return results