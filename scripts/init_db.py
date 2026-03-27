"""
数据库初始化脚本
初始化数据库表结构，可在首次运行前执行
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import init_database


def main():
    """
    主函数
    """
    print("开始初始化数据库...")
    try:
        init_database()
        print("数据库初始化成功！")
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()