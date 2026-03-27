"""
测试信息抽取模块
使用parser生成的JSON文件作为输入
"""
import os
import json
from app.services.extractor import extract_entities

# 输入目录（parser的输出）
INPUT_DIR = "data/test_output"
# 输出目录
OUTPUT_DIR = "data/test_output"

def test_extractor():
    """测试信息抽取功能"""
    print("开始测试信息抽取模块...\n")
    
    # 获取所有JSON文件
    json_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.json') and f != 'parser_test_summary.json']
    
    all_entities = []
    
    for json_file in json_files:
        json_path = os.path.join(INPUT_DIR, json_file)
        
        print(f"处理文件: {json_file}")
        print("-" * 50)
        
        try:
            # 读取解析后的文档
            with open(json_path, 'r', encoding='utf-8') as f:
                parsed_doc = json.load(f)
            
            # 执行信息抽取
            entities = extract_entities(parsed_doc)
            all_entities.extend(entities)
            
            # 打印抽取结果
            print(f"抽取到 {len(entities)} 个实体")
            
            # 按类型分组显示
            entity_types = {}
            for entity in entities:
                etype = entity['entity_type']
                if etype not in entity_types:
                    entity_types[etype] = []
                entity_types[etype].append(entity['value'])
            
            for etype, values in entity_types.items():
                print(f"\n{etype} ({len(values)}个):")
                # 显示前5个不同的值
                unique_values = list(set(values))[:5]
                for val in unique_values:
                    print(f"  - {val}")
                if len(set(values)) > 5:
                    print(f"  ... 还有 {len(set(values)) - 5} 个不同的值")
            
            # 保存抽取结果
            output_filename = f"{os.path.splitext(json_file)[0]}_entities.json"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(entities, f, ensure_ascii=False, indent=2)
            print(f"\n实体已保存: {output_filename}")
            
            print("\n" + "=" * 50 + "\n")
            
        except Exception as e:
            print(f"处理失败: {e}\n")
    
    # 保存所有实体的汇总
    summary_path = os.path.join(OUTPUT_DIR, "extractor_test_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(all_entities, f, ensure_ascii=False, indent=2)
    
    print(f"\n抽取汇总已保存: {summary_path}")
    print(f"共从 {len(json_files)} 个文档中抽取 {len(all_entities)} 个实体")
    
    return all_entities

if __name__ == "__main__":
    test_extractor()
