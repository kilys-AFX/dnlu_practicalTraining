"""
初始化 MySQL 数据库
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from data.database import init_database

if __name__ == "__main__":
    print("正在初始化 MySQL 数据库...")
    init_database()
    print("初始化完成！")
