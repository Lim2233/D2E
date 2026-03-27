"""
辅助函数模块
存放通用辅助函数（如文件读写、文本清洗、格式转换）
"""
import re
import os
from typing import List, Dict, Any


def clean_text(text: str) -> str:
    """
    清理文本
    
    Args:
        text: 原始文本
    
    Returns:
        清理后的文本
    """
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    
    # 移除特殊字符（保留中文、英文、数字、常见标点）
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？；：、"\'()（）【】]', ' ', text)
    
    # 去除首尾空白
    text = text.strip()
    
    return text


def normalize_amount(amount: str) -> str:
    """
    归一化金额
    
    Args:
        amount: 金额字符串
    
    Returns:
        归一化后的金额字符串
    """
    # 移除货币符号
    amount = re.sub(r'[¥￥$\$]', '', amount)
    
    # 移除逗号
    amount = amount.replace(',', '')
    
    # 去除空白
    amount = amount.strip()
    
    return amount


def normalize_date(date: str) -> str:
    """
    归一化日期
    
    Args:
        date: 日期字符串
    
    Returns:
        归一化后的日期字符串（YYYY-MM-DD）
    """
    # 处理不同格式的日期
    patterns = [
        r'(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})日?',
        r'(\d{4})(\d{2})(\d{2})'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, date)
        if match:
            year, month, day = match.groups()
            # 确保月份和日期是两位数
            month = month.zfill(2)
            day = day.zfill(2)
            return f"{year}-{month}-{day}"
    
    return date


def ensure_directory(directory: str):
    """
    确保目录存在
    
    Args:
        directory: 目录路径
    """
    os.makedirs(directory, exist_ok=True)


def get_file_extension(filename: str) -> str:
    """
    获取文件扩展名
    
    Args:
        filename: 文件名
    
    Returns:
        小写的文件扩展名（包含点号）
    """
    return os.path.splitext(filename)[1].lower()