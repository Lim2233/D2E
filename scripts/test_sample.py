"""
测试脚本
用于测试完整的系统流程
"""
import sys
import os
import tempfile

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import init_database
from backend.app.services.parser import parse_document
from backend.app.services.extractor import extract_entities
from backend.app.services.matcher import match_entities
from backend.app.services.filler import fill_template, extract_template_fields
from backend.app.services.knowledge_pool import KnowledgePool


def test_complete_flow():
    """
    测试完整的系统流程
    """
    print("开始测试完整系统流程...")
    
    try:
        # 1. 初始化数据库
        print("1. 初始化数据库...")
        init_database()
        print("数据库初始化成功！")
        
        # 2. 创建知识池实例
        knowledge_pool = KnowledgePool()
        
        # 3. 选择测试文档（使用 txt 文件作为示例）
        test_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'backend', 'data', 'test_set', 'txt', '2024年国民经济和社会发展统计公报（节选）.txt'
        )
        
        if not os.path.exists(test_doc_path):
            print(f"测试文档不存在: {test_doc_path}")
            return
        
        print(f"2. 使用测试文档: {os.path.basename(test_doc_path)}")
        
        # 4. 解析文档
        print("3. 解析文档...")
        parsed_doc = parse_document(test_doc_path)
        print(f"文档解析成功，ID: {parsed_doc['doc_id']}")
        print(f"段落数量: {len(parsed_doc['paragraphs'])}")
        print(f"表格数量: {len(parsed_doc['tables'])}")
        
        # 5. 提取实体
        print("4. 提取实体...")
        entities = extract_entities(parsed_doc)
        print(f"提取到 {len(entities)} 个实体")
        
        # 6. 保存到知识池
        print("5. 保存到知识池...")
        knowledge_pool.save_document(parsed_doc['doc_id'], parsed_doc, entities)
        print("保存成功！")
        
        # 7. 从知识池获取实体
        print("6. 从知识池获取实体...")
        saved_entities = knowledge_pool.get_entities_by_doc_id(parsed_doc['doc_id'])
        print(f"从知识池获取到 {len(saved_entities)} 个实体")
        
        # 8. 测试语义匹配
        print("7. 测试语义匹配...")
        test_fields = ["GDP", "增长率", "人口", "财政收入"]
        matches = match_entities(test_fields, saved_entities)
        print(f"匹配结果: {matches}")
        
        # 9. 测试模板填充（使用临时模板）
        print("8. 测试模板填充...")
        
        # 创建临时 Excel 模板
        import pandas as pd
        
        template_df = pd.DataFrame({
            '字段': test_fields,
            '值': [''] * len(test_fields)
        })
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            template_path = tmp.name
        
        template_df.to_excel(template_path, index=False)
        
        try:
            # 提取模板字段
            template_fields = extract_template_fields(template_path)
            print(f"模板字段: {template_fields}")
            
            # 匹配实体
            matches = match_entities(template_fields, saved_entities)
            
            # 填充模板
            output_path = fill_template(template_path, matches)
            print(f"填充成功，输出文件: {output_path}")
            
            # 读取填充后的文件
            filled_df = pd.read_excel(output_path)
            print("填充结果:")
            print(filled_df)
            
        finally:
            # 清理临时文件
            if os.path.exists(template_path):
                os.remove(template_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        
        print("\n测试完成！")
        
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()


def test_document_parsing():
    """
    测试文档解析
    """
    print("\n测试文档解析...")
    
    # 测试不同格式的文档
    test_files = [
        os.path.join('backend', 'data', 'test_set', 'txt', '2024年国民经济和社会发展统计公报（节选）.txt'),
        os.path.join('backend', 'data', 'test_set', 'md', '2023年文化和旅游发展统计公报.md'),
        os.path.join('backend', 'data', 'test_set', 'Excel', '电商销售数据.xlsx'),
        os.path.join('backend', 'data', 'test_set', 'word', '2021年民政事业发展统计公报.docx')
    ]
    
    for file_path in test_files:
        full_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            file_path
        )
        
        if not os.path.exists(full_path):
            print(f"文件不存在: {file_path}")
            continue
        
        print(f"\n解析文件: {os.path.basename(full_path)}")
        
        try:
            parsed_doc = parse_document(full_path)
            print(f"- 文档 ID: {parsed_doc['doc_id']}")
            print(f"- 段落数量: {len(parsed_doc['paragraphs'])}")
            print(f"- 表格数量: {len(parsed_doc['tables'])}")
            print(f"- 原始文本长度: {len(parsed_doc['raw_text'])}")
        except Exception as e:
            print(f"解析失败: {e}")


if __name__ == "__main__":
    # 测试完整流程
    test_complete_flow()
    
    # 测试文档解析
    test_document_parsing()