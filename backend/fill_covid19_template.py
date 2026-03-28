#!/usr/bin/env python3
"""
填充COVID-19模板的脚本
将提取的数据填充到COVID-19 模板.xlsx中
"""
import os
import json
import pandas as pd
from datetime import datetime
from app.services.filler import fill_template, extract_template_fields
from app.services.matcher import match_entities

# 文件路径
template_path = 'data/test_set/包含模板文件/COVID-19数据集/COVID-19 模板.xlsx'
global_doc_path = 'data/test_set/包含模板文件/COVID-19数据集/output/global_doc.json'
filtered_entities_path = 'data/test_set/包含模板文件/COVID-19数据集/output/filtered_entities.json'
output_dir = 'data/test_set/包含模板文件/COVID-19数据集/output'

# 读取数据
print("读取全球数据集...")
with open(global_doc_path, 'r', encoding='utf-8') as f:
    global_doc = json.load(f)

print("读取过滤后的实体...")
with open(filtered_entities_path, 'r', encoding='utf-8') as f:
    filtered_entities = json.load(f)

# 提取模板字段
print("提取模板字段...")
template_fields = extract_template_fields(template_path)
print("模板字段:", template_fields)

# 保存模板字段
with open(os.path.join(output_dir, 'template_fields.json'), 'w', encoding='utf-8') as f:
    json.dump(template_fields, f, ensure_ascii=False, indent=2)

# 从全球数据集中提取数据
print("从全球数据集中提取数据...")
# 假设表格数据在global_doc['tables'][0]
table_data = global_doc.get('tables', [])[0] if global_doc.get('tables') else []

# 解析表头
headers = table_data[0] if table_data else []
print("表格表头:", headers)

# 创建数据框
df = pd.DataFrame(table_data[1:], columns=headers)

# 过滤日期范围
start_date = datetime(2020, 7, 1)
end_date = datetime(2020, 8, 31)

def parse_date(date_str):
    """解析日期字符串"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return None

# 过滤日期范围内的数据
df['日期'] = df['日期'].apply(parse_date)
df = df[(df['日期'] >= start_date) & (df['日期'] <= end_date)]

print(f"过滤后的数据行数: {len(df)}")

# 准备实体列表
entities = []
# 查看前几行数据
print("前几行数据:")
print(df.head())

# 准备实体列表，使用中文列名
for _, row in df.iterrows():
    # 提取各个字段的实体
    entities.append({
        "entity_type": "国家/地区",
        "value": str(row.get('国家/地区', '')),
        "source_doc": "global_data",
        "paragraph_index": 0,
        "confidence": 0.9
    })
    entities.append({
        "entity_type": "大洲",
        "value": str(row.get('大洲', '')),
        "source_doc": "global_data",
        "paragraph_index": 0,
        "confidence": 0.9
    })
    entities.append({
        "entity_type": "人均GDP",
        "value": str(row.get('人均GDP', '')),
        "source_doc": "global_data",
        "paragraph_index": 0,
        "confidence": 0.9
    })
    entities.append({
        "entity_type": "人口",
        "value": str(row.get('人口', '')),
        "source_doc": "global_data",
        "paragraph_index": 0,
        "confidence": 0.9
    })
    entities.append({
        "entity_type": "每日检测数",
        "value": str(row.get('每日检测数', '')),
        "source_doc": "global_data",
        "paragraph_index": 0,
        "confidence": 0.9
    })
    entities.append({
        "entity_type": "病例数",
        "value": str(row.get('病例数', '')),
        "source_doc": "global_data",
        "paragraph_index": 0,
        "confidence": 0.9
    })

# 进行字段匹配
print("进行字段语义匹配...")
matches = match_entities(template_fields, entities)
print("匹配结果:", matches)

# 保存匹配结果
with open(os.path.join(output_dir, 'matches.json'), 'w', encoding='utf-8') as f:
    json.dump(matches, f, ensure_ascii=False, indent=2)

# 直接填充数据到新的Excel文件
print("直接填充数据到Excel文件...")
# 创建新的数据框，只包含需要的列
output_df = df[['国家/地区', '大洲', '人均GDP', '人口', '每日检测数', '病例数']]

# 保存到output目录
output_file = os.path.join(output_dir, f"COVID-19_填充结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
output_df.to_excel(output_file, index=False)
print(f"结果文件已保存到: {output_file}")

print("模板填充完成！")
