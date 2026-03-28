#!/usr/bin/env python3
"""
测试COVID-19数据集处理（日期范围）
按照用户要求处理2020/7/1到2020/8/31的日期数据并填充模板
"""
import os
import json
import pandas as pd
from datetime import datetime
from app.services.parser import parse_document
from app.services.extractor import extract_entities
from app.services.filler import fill_template, extract_template_fields
from app.services.matcher import match_entities
from app.services.knowledge_pool import KnowledgePool

# 数据集路径
DATASET_PATH = "d:\\workspace\\Projects\\2026fwwb\\D2E\\backend\\data\\test_set\\包含模板文件\\COVID-19数据集"
USER_REQUEST_FILE = os.path.join(DATASET_PATH, "用户要求.txt")
CHINA_DOCX = os.path.join(DATASET_PATH, "中国COVID-19新冠疫情情况.docx")
GLOBAL_XLSX = os.path.join(DATASET_PATH, "COVID-19全球数据集（节选）.xlsx")
TEMPLATE_XLSX = os.path.join(DATASET_PATH, "COVID-19 模板.xlsx")
OUTPUT_DIR = os.path.join(DATASET_PATH, "output")

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_user_request():
    """加载用户要求"""
    with open(USER_REQUEST_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def extract_date_range_data():
    """提取2020/7/1到2020/8/31的日期数据"""
    # 解析全球数据集
    print("解析全球COVID-19数据集...")
    global_doc = parse_document(GLOBAL_XLSX)
    
    # 从表格中提取数据
    date_range_data = []
    if global_doc.get('tables'):
        # 假设第一个表格包含数据
        table = global_doc['tables'][0]
        headers = table[0]
        
        # 找到日期列的索引
        date_col_index = None
        cases_col_index = None
        tests_col_index = None
        
        for i, header in enumerate(headers):
            if '日期' in header or 'date' in header.lower():
                date_col_index = i
            elif '病例' in header or 'cases' in header.lower():
                cases_col_index = i
            elif '检测' in header or 'tests' in header.lower():
                tests_col_index = i
        
        if date_col_index is not None:
            # 遍历数据行
            for row in table[1:]:
                if len(row) > date_col_index:
                    date_str = row[date_col_index]
                    try:
                        # 解析日期
                        if ' ' in date_str:
                            date_str = date_str.split(' ')[0]
                        if '-' in date_str:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        elif '/' in date_str:
                            date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                        else:
                            continue
                        
                        # 检查日期是否在范围内
                        start_date = datetime(2020, 7, 1)
                        end_date = datetime(2020, 8, 31)
                        if start_date <= date_obj <= end_date:
                            # 提取相关数据
                            data = {
                                'date': date_obj.strftime('%Y/%m/%d'),
                                'country': row[0] if len(row) > 0 else '',
                                'continent': row[1] if len(row) > 1 else '',
                                'cases': row[cases_col_index] if cases_col_index and len(row) > cases_col_index else '',
                                'tests': row[tests_col_index] if tests_col_index and len(row) > tests_col_index else ''
                            }
                            date_range_data.append(data)
                    except Exception as e:
                        pass
    
    return date_range_data

def process_documents():
    """处理文档"""
    # 1. 加载用户要求
    user_request = load_user_request()
    print(f"用户要求: {user_request}")
    
    # 2. 提取日期范围数据
    date_range_data = extract_date_range_data()
    print(f"提取到 {len(date_range_data)} 条2020/7/1到2020/8/31的记录")
    
    # 3. 保存提取的数据
    with open(os.path.join(OUTPUT_DIR, "date_range_data.json"), 'w', encoding='utf-8') as f:
        json.dump(date_range_data, f, ensure_ascii=False, indent=2)
    
    # 4. 读取模板
    print("读取模板...")
    template_fields = extract_template_fields(TEMPLATE_XLSX)
    print(f"模板字段: {template_fields}")
    
    # 5. 准备填充数据
    # 这里我们直接使用提取的数据填充模板
    # 由于模板结构可能不同，我们创建一个简单的匹配
    matches = {}
    
    # 示例：填充第一条数据
    if date_range_data:
        first_data = date_range_data[0]
        # 假设模板字段与数据字段对应
        for field in template_fields:
            if '国家' in field or '地区' in field:
                matches[field] = {
                    "entity": {
                        "entity_type": "国家/地区",
                        "value": first_data['country'],
                        "source_doc": "global_data",
                        "paragraph_index": 0,
                        "confidence": 0.9
                    },
                    "score": 0.9
                }
            elif '大洲' in field:
                matches[field] = {
                    "entity": {
                        "entity_type": "大洲",
                        "value": first_data['continent'],
                        "source_doc": "global_data",
                        "paragraph_index": 0,
                        "confidence": 0.9
                    },
                    "score": 0.9
                }
            elif '病例' in field:
                matches[field] = {
                    "entity": {
                        "entity_type": "病例数",
                        "value": str(first_data['cases']),
                        "source_doc": "global_data",
                        "paragraph_index": 0,
                        "confidence": 0.9
                    },
                    "score": 0.9
                }
            elif '检测' in field:
                matches[field] = {
                    "entity": {
                        "entity_type": "每日检测数",
                        "value": str(first_data['tests']),
                        "source_doc": "global_data",
                        "paragraph_index": 0,
                        "confidence": 0.9
                    },
                    "score": 0.9
                }
    
    # 6. 保存匹配结果
    with open(os.path.join(OUTPUT_DIR, "date_matches.json"), 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    
    # 7. 填充模板
    print("填充模板...")
    output_path = fill_template(TEMPLATE_XLSX, matches)
    
    # 复制结果到输出目录
    result_filename = f"COVID-19_日期范围填充结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    result_path = os.path.join(OUTPUT_DIR, result_filename)
    import shutil
    shutil.copy2(output_path, result_path)
    
    # 8. 生成完整的日期范围数据表格
    if date_range_data:
        df = pd.DataFrame(date_range_data)
        excel_path = os.path.join(OUTPUT_DIR, "COVID-19_2020-07-01_2020-08-31数据.xlsx")
        df.to_excel(excel_path, index=False)
        print(f"完整日期范围数据已保存到: {excel_path}")
    
    print(f"\n处理完成！")
    print(f"结果文件: {result_path}")
    print(f"所有过程文件保存在: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_documents()
