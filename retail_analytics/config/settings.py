"""
配置文件 - 智能零售用户行为分析系统
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 数据库配置
DATABASE_PATH = BASE_DIR / "data" / "retail.db"

# MySQL 配置（切换到 MySQL 时需要填写）
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_password",  # 请填写您的 MySQL 密码
    "database": "retail_analytics",
    "charset": "utf8mb4"
}

# 使用数据库类型：'sqlite' 或 'mysql'
DB_TYPE = "sqlite"  # 改为 "mysql" 启用 MySQL

# MiMo API 配置（需要用户填写）
MIMO_CONFIG = {
    "api_key": "",  # 请填写你的 MiMo API Key
    "base_url": "",  # 请填写 base_url
    "model": "",  # 请填写模型名称
}

# 应用配置
APP_CONFIG = {
    "title": "智能零售用户行为分析系统",
    "icon": "🛒",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "theme_primary_color": "#1E88E5",
    "theme_secondary_color": "#FF6F00",
}

# 数据配置
DATA_CONFIG = {
    "max_upload_size_mb": 200,
    "supported_formats": [".csv", ".xlsx", ".xls"],
    "default_date_range_days": 30,
}

# 模型配置
MODEL_CONFIG = {
    "models_dir": BASE_DIR / "models",
    "default_epochs": 50,
    "batch_size": 32,
    "learning_rate": 0.001,
    "test_size": 0.2,
    "random_state": 42,
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}
