#!/usr/bin/env python3
"""
测试基本的 Python 功能
"""
import os
import sys
import tempfile

print(f"Python 版本: {sys.version}")
print(f"平台: {sys.platform}")
print(f"当前目录: {os.getcwd()}")

# 测试文件操作
try:
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
        tmp.write(b'Hello, World!')
        temp_path = tmp.name
    print(f"临时文件创建成功: {temp_path}")
    
    with open(temp_path, 'r') as f:
        content = f.read()
    print(f"临时文件读取成功: {content}")
    
    os.unlink(temp_path)
    print("临时文件删除成功")
except Exception as e:
    print(f"文件操作失败: {e}")

# 测试模块导入
try:
    import math
    print(f"math 模块导入成功: pi = {math.pi}")
except Exception as e:
    print(f"math 模块导入失败: {e}")

try:
    import json
    test_dict = {"key": "value"}
    json_str = json.dumps(test_dict)
    print(f"json 模块导入成功: {json_str}")
except Exception as e:
    print(f"json 模块导入失败: {e}")

print("基本功能测试完成")
