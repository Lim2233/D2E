#!/usr/bin/env python3
"""
测试 asyncio 导入
"""
import sys
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")

# 尝试导入 asyncio
try:
    import asyncio
    print("asyncio 导入成功")
except Exception as e:
    print(f"asyncio 导入失败: {e}")
    import traceback
    traceback.print_exc()
