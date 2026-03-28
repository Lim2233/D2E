#!/usr/bin/env python3
"""
提取COVID-19数据的脚本
从指定文件中提取2020/7/1到2020/8/31日期范围内的数据
"""
import os
import json
from app.services.parser import parse_document
from app.services.extractor import extract_entities
from datetime import datetime

# 文件路径
china_doc_path = 'data/test_set/包含模板文件/COVID-19数据集/中国COVID-19新冠疫情情况.docx'
global_xlsx_path = 'data/test_set/包含模板文件/COVID-19数据集/COVID-19全球数据集（节选）.xlsx'
output_dir = 'data/test_set/包含模板文件/COVID-19数据集/output'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 解析文档
print("解析中国COVID-19新冠疫情情况.docx...")
china_doc = parse_document(china_doc_path)
print("解析COVID-19全球数据集（节选）.xlsx...")
global_doc = parse_document(global_xlsx_path)

# 保存解析结果
with open(os.path.join(output_dir, 'china_doc.json'), 'w', encoding='utf-8') as f:
    json.dump(china_doc, f, ensure_ascii=False, indent=2)
with open(os.path.join(output_dir, 'global_doc.json'), 'w', encoding='utf-8') as f:
    json.dump(global_doc, f, ensure_ascii=False, indent=2)

# 提取实体
print("提取中国文档中的实体...")
china_entities = extract_entities(china_doc)
print("提取全球数据集文档中的实体...")
global_entities = extract_entities(global_doc)

# 保存提取结果
with open(os.path.join(output_dir, 'china_entities.json'), 'w', encoding='utf-8') as f:
    json.dump(china_entities, f, ensure_ascii=False, indent=2)
with open(os.path.join(output_dir, 'global_entities.json'), 'w', encoding='utf-8') as f:
    json.dump(global_entities, f, ensure_ascii=False, indent=2)

# 合并实体
all_entities = china_entities + global_entities
with open(os.path.join(output_dir, 'all_entities.json'), 'w', encoding='utf-8') as f:
    json.dump(all_entities, f, ensure_ascii=False, indent=2)

# 过滤指定日期范围的数据
def parse_date(date_str):
    """解析日期字符串"""
    # 尝试不同的日期格式
    formats = ['%Y/%m/%d', '%Y-%m-%d', '%Y年%m月%d日']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

start_date = datetime(2020, 7, 1)
end_date = datetime(2020, 8, 31)

filtered_entities = []
for entity in all_entities:
    if entity['entity_type'] == '日期':
        date = parse_date(entity['value'])
        if date and start_date <= date <= end_date:
            filtered_entities.append(entity)

print(f"提取到 {len(filtered_entities)} 个在2020/7/1到2020/8/31范围内的日期实体")

# 保存过滤结果
with open(os.path.join(output_dir, 'filtered_entities.json'), 'w', encoding='utf-8') as f:
    json.dump(filtered_entities, f, ensure_ascii=False, indent=2)

print("数据提取完成，结果保存在output目录中")
