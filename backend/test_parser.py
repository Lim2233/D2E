"""
测试文档解析模块
"""
import os
import json
from app.services.parser import parse_document

# 测试文件路径
test_files = [
    # Word文档
    "data/test_set/word/2021年民政事业发展统计公报.docx",
    # Excel文档
    "data/test_set/Excel/2025年国考职位表（节选）.xlsx",
    # Markdown文档
    "data/test_set/md/2024年卫生健康事业发展统计公报.md",
    # TXT文档
    "data/test_set/txt/2024年国民经济和社会发展统计公报（节选）.txt"
]

# 输出目录
OUTPUT_DIR = "data/test_output"

def test_parser():
    """测试文档解析功能"""
    print("开始测试文档解析模块...\n")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    results = []
    
    for file_path in test_files:
        # 获取绝对路径
        absolute_path = os.path.abspath(file_path)
        
        if not os.path.exists(absolute_path):
            print(f"文件不存在: {absolute_path}")
            continue
        
        print(f"测试文件: {file_path}")
        print(f"绝对路径: {absolute_path}")
        print(f"文件大小: {os.path.getsize(absolute_path)} 字节")
        print("-" * 50)
        
        try:
            # 执行解析
            result = parse_document(absolute_path)
            results.append(result)
            
            # 打印解析结果
            print(f"文档ID: {result['doc_id']}")
            print(f"段落数量: {len(result['paragraphs'])}")
            print(f"表格数量: {len(result['tables'])}")
            print(f"原始文本长度: {len(result['raw_text'])} 字符")
            
            # 打印前3个段落（如果有）
            if result['paragraphs']:
                print("\n前3个段落:")
                for i, para in enumerate(result['paragraphs'][:3], 1):
                    print(f"{i}. {para[:100]}..." if len(para) > 100 else f"{i}. {para}")
            
            # 打印第一个表格（如果有）
            if result['tables']:
                print("\n第一个表格:")
                table = result['tables'][0]
                for i, row in enumerate(table[:3], 1):  # 只显示前3行
                    print(f"行 {i}: {row}")
                if len(table) > 3:
                    print(f"... 共 {len(table)} 行")
            
            # 保存JSON文件
            filename = os.path.basename(file_path)
            json_filename = f"{os.path.splitext(filename)[0]}.json"
            json_path = os.path.join(OUTPUT_DIR, json_filename)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\nJSON已保存: {json_path}")
            
            print("解析成功!\n")
            
        except Exception as e:
            print(f"解析失败: {e}\n")
    
    # 保存汇总结果
    summary_path = os.path.join(OUTPUT_DIR, "parser_test_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n测试汇总已保存: {summary_path}")
    print(f"共测试 {len(results)} 个文件")
    
    return results

if __name__ == "__main__":
    test_parser()
