#!/usr/bin/env python3
"""
启动脚本，解决 Python 3.13 在 Windows 下的 asyncio 问题
"""
import os
import sys

# 解决 Python 3.13 在 Windows 下的 asyncio 问题
if sys.platform == 'win32':
    # 强制使用 SelectorEventLoop
    os.environ['PYTHONASYNCIODEBUG'] = '1'
    os.environ['PYTHONUNBUFFERED'] = '1'

# 导入并运行应用
from app.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
