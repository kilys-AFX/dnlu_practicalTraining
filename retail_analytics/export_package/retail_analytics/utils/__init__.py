"""
工具函数模块
"""
from .data_processor import clean_data, kmeans_clustering, calculate_retention, get_behavior_funnel, generate_session_data

# 可选导入calculate_rfm（如果不存在则忽略）
try:
    from .data_processor import calculate_rfm
    __all__ = ["clean_data", "calculate_rfm", "kmeans_clustering", "calculate_retention", "get_behavior_funnel", "generate_session_data"]
except ImportError:
    __all__ = ["clean_data", "kmeans_clustering", "calculate_retention", "get_behavior_funnel", "generate_session_data"]
