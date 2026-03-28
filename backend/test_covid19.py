#!/usr/bin/env python3
"""
测试COVID-19数据集处理
按照用户要求处理文档并填充模板
"""
import os
import json
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

def process_documents():
    """处理文档"""
    # 1. 加载用户要求
    user_request = load_user_request()
    print(f"用户要求: {user_request}")
    
    # 2. 解析文档
    print("\n解析中国COVID-19新冠疫情情况.docx...")
    china_doc = parse_document(CHINA_DOCX)
    
    print("解析COVID-19全球数据集（节选）.xlsx...")
    global_doc = parse_document(GLOBAL_XLSX)
    
    # 保存解析结果
    with open(os.path.join(OUTPUT_DIR, "china_doc.json"), 'w', encoding='utf-8') as f:
        json.dump(china_doc, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(OUTPUT_DIR, "global_doc.json"), 'w', encoding='utf-8') as f:
        json.dump(global_doc, f, ensure_ascii=False, indent=2)
    
    # 3. 抽取实体
    print("\n从中国COVID-19文档中抽取实体...")
    china_entities = extract_entities(china_doc)
    
    print("从全球COVID-19数据集中抽取实体...")
    global_entities = extract_entities(global_doc)
    
    # 合并实体
    all_entities = china_entities + global_entities
    
    # 保存实体结果
    with open(os.path.join(OUTPUT_DIR, "china_entities.json"), 'w', encoding='utf-8') as f:
        json.dump(china_entities, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(OUTPUT_DIR, "global_entities.json"), 'w', encoding='utf-8') as f:
        json.dump(global_entities, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(OUTPUT_DIR, "all_entities.json"), 'w', encoding='utf-8') as f:
        json.dump(all_entities, f, ensure_ascii=False, indent=2)
    
    # 4. 提取模板字段
    print("\n提取模板字段...")
    template_fields = extract_template_fields(TEMPLATE_XLSX)
    print(f"模板字段: {template_fields}")
    
    # 保存模板字段
    with open(os.path.join(OUTPUT_DIR, "template_fields.json"), 'w', encoding='utf-8') as f:
        json.dump(template_fields, f, ensure_ascii=False, indent=2)
    
    # 5. 语义匹配
    print("\n进行语义匹配...")
    matches = match_entities(template_fields, all_entities)
    
    # 保存匹配结果
    with open(os.path.join(OUTPUT_DIR, "matches.json"), 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    
    # 6. 填充模板
    print("\n填充模板...")
    output_path = fill_template(TEMPLATE_XLSX, matches)
    
    # 复制结果到输出目录
    result_filename = f"COVID-19_填充结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    result_path = os.path.join(OUTPUT_DIR, result_filename)
    import shutil
    shutil.copy2(output_path, result_path)
    
    # 7. 保存到知识池
    print("\n保存到知识池...")
    knowledge_pool = KnowledgePool()
    knowledge_pool.save_document(china_doc['doc_id'], china_doc, china_entities)
    knowledge_pool.save_document(global_doc['doc_id'], global_doc, global_entities)
    
    print(f"\n处理完成！")
    print(f"结果文件: {result_path}")
    print(f"所有过程文件保存在: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_documents()
