"""
文本向量化模块
封装 SentenceTransformer 用于语义匹配
"""
from sentence_transformers import SentenceTransformer, util
import numpy as np
from typing import List, Optional


class TextVectorizer:
    """
    文本向量化类
    """
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """
        初始化文本向量化器
        
        Args:
            model_name: 预训练模型名称
        """
        try:
            self.model = SentenceTransformer(model_name)
            self.available = True
        except Exception as e:
            print(f"加载模型失败: {e}")
            self.model = None
            self.available = False
    
    def vectorize(self, text: str) -> Optional[np.ndarray]:
        """
        将文本转换为向量
        
        Args:
            text: 输入文本
        
        Returns:
            文本向量，如果模型不可用则返回 None
        """
        if not self.available:
            return None
        
        try:
            return self.model.encode(text)
        except Exception as e:
            print(f"向量化失败: {e}")
            return None
    
    def vectorize_batch(self, texts: List[str]) -> Optional[np.ndarray]:
        """
        批量将文本转换为向量
        
        Args:
            texts: 文本列表
        
        Returns:
            文本向量矩阵，如果模型不可用则返回 None
        """
        if not self.available:
            return None
        
        try:
            return self.model.encode(texts)
        except Exception as e:
            print(f"批量向量化失败: {e}")
            return None
    
    def calculate_similarity(self, text1: str, text2: str) -> Optional[float]:
        """
        计算两个文本的相似度
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
        
        Returns:
            相似度分数（0-1），如果模型不可用则返回 None
        """
        if not self.available:
            return None
        
        try:
            vec1 = self.vectorize(text1)
            vec2 = self.vectorize(text2)
            if vec1 is None or vec2 is None:
                return None
            
            # 计算余弦相似度
            return util.cos_sim(vec1, vec2).item()
        except Exception as e:
            print(f"计算相似度失败: {e}")
            return None
    
    def calculate_similarity_batch(self, text: str, texts: List[str]) -> Optional[List[float]]:
        """
        计算一个文本与多个文本的相似度
        
        Args:
            text: 单个文本
            texts: 文本列表
        
        Returns:
            相似度分数列表，如果模型不可用则返回 None
        """
        if not self.available:
            return None
        
        try:
            vec = self.vectorize(text)
            vecs = self.vectorize_batch(texts)
            if vec is None or vecs is None:
                return None
            
            # 计算余弦相似度
            similarities = util.cos_sim(vec, vecs)[0].tolist()
            return similarities
        except Exception as e:
            print(f"批量计算相似度失败: {e}")
            return None


# 创建全局向量器实例
vectorizer = TextVectorizer()