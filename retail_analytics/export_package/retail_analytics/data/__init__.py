"""
数据层模块
"""
from .database import init_database, get_connection, execute_query, bulk_insert
from .data_generator import generate_all_data, generate_users, generate_products, generate_orders, generate_user_behavior

__all__ = [
    "init_database",
    "get_connection",
    "execute_query",
    "bulk_insert",
    "generate_all_data",
    "generate_users",
    "generate_products",
    "generate_orders",
    "generate_user_behavior"
]
