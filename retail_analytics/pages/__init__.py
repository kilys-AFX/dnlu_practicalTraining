"""
Pages Module - All page modules
"""
from .data_management import show_data_upload_page, show_data_preview_page, show_data_clean_page
from .data_overview import show_key_metrics_page, show_trend_analysis_page, show_user_portrait_page
from .behavior_analysis import show_heatmap_page, show_funnel_page, show_retention_page, show_behavior_path_page
from .user_profiling import show_clustering_page, show_lifecycle_page
from .ai_assistant import show_ai_chat_page, show_report_page
from .prediction_models import show_purchase_intent_page, show_sales_forecast_page
from .realtime_dashboard import show_realtime_dashboard
from .anomaly_detection import show_anomaly_detection_page
from .pdf_export import show_pdf_export_page
from .data_integration import show_csv_connector, show_excel_connector, show_api_connector
from .system_management import show_user_management_page, show_system_logs_page

__all__ = [
    "show_data_upload_page",
    "show_data_preview_page",
    "show_data_clean_page",
    "show_key_metrics_page",
    "show_trend_analysis_page",
    "show_user_portrait_page",
    "show_heatmap_page",
    "show_funnel_page",
    "show_retention_page",
    "show_behavior_path_page",
    "show_clustering_page",
    "show_lifecycle_page",
    "show_ai_chat_page",
    "show_report_page",
    "show_purchase_intent_page",
    "show_sales_forecast_page",
    "show_realtime_dashboard",
    "show_anomaly_detection_page",
    "show_pdf_export_page",
    "show_csv_connector",
    "show_excel_connector",
    "show_api_connector",
    "show_user_management_page",
    "show_system_logs_page"
]
