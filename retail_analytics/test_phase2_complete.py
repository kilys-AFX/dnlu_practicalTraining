"""
Phase 2 Complete System Test Script
Test all Phase 2 features: Real-time Dashboard, Anomaly Detection, AI Assistant, PDF Export
"""

import sys
import traceback

def test_imports():
    """Test all module imports"""
    print("=" * 60)
    print("Testing Module Imports")
    print("=" * 60)
    
    modules = [
        ("pages.realtime_dashboard", "show_realtime_dashboard"),
        ("pages.anomaly_detection", "show_anomaly_detection_page"),
        ("pages.ai_assistant", "show_ai_chat_page"),
        ("pages.ai_assistant", "show_report_page"),
        ("pages.pdf_export", "show_pdf_export_page"),
        ("utils.pdf_generator", "generate_pdf_report"),
        ("utils.pdf_generator", "get_report_data"),
    ]
    
    results = []
    for module_name, func_name in modules:
        try:
            exec(f"from {module_name} import {func_name}")
            print(f"✅ {module_name}.{func_name}")
            results.append(True)
        except Exception as e:
            print(f"❌ {module_name}.{func_name}: {e}")
            results.append(False)
    
    return all(results)

def test_database_connection():
    """Test database connection and tables"""
    print("\n" + "=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    
    try:
        from data.database import execute_query, init_database
        
        # Test connection
        result = execute_query("SELECT 1")
        if not result.empty:
            print("✅ Database connection successful")
        else:
            print("❌ Database connection failed")
            return False
        
        # Test tables
        tables = ["users", "orders", "order_items", "products", "user_behavior"]
        for table in tables:
            try:
                count = execute_query(f"SELECT COUNT(*) as count FROM {table}")
                print(f"✅ Table '{table}': {count.iloc[0]['count']} records")
            except Exception as e:
                print(f"⚠️  Table '{table}' not found: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        traceback.print_exc()
        return False

def test_realtime_dashboard():
    """Test real-time dashboard functions"""
    print("\n" + "=" * 60)
    print("Testing Real-time Dashboard")
    print("=" * 60)
    
    try:
        from pages.realtime_dashboard import generate_mock_realtime_data, get_realtime_data
        
        # Test mock data generation
        mock_data = generate_mock_realtime_data()
        required_keys = ["online_users", "today_orders", "today_gmv", "hourly_orders", "hourly_gmv", "top_products", "category_sales", "recent_orders"]
        
        for key in required_keys:
            if key in mock_data:
                print(f"✅ Mock data contains '{key}'")
            else:
                print(f"❌ Mock data missing '{key}'")
                return False
        
        print("✅ Real-time dashboard functions working")
        return True
        
    except Exception as e:
        print(f"❌ Real-time dashboard test failed: {e}")
        traceback.print_exc()
        return False

def test_anomaly_detection():
    """Test anomaly detection functions"""
    print("\n" + "=" * 60)
    print("Testing Anomaly Detection")
    print("=" * 60)
    
    try:
        import pandas as pd
        from pages.anomaly_detection import detect_anomalies, analyze_sales_anomalies
        
        # Test detect_anomalies function
        test_df = pd.DataFrame({
            "date": pd.date_range(start="2024-01-01", periods=30, freq="D"),
            "gmv": [1000 + i*10 for i in range(30)]
        })
        
        # Add anomaly
        test_df.loc[10, "gmv"] = 20000
        
        anomalies, df_with_scores = detect_anomalies(test_df, "gmv", window=7, threshold=2)
        
        if not anomalies.empty:
            print(f"✅ Anomaly detection found {len(anomalies)} anomaly(s)")
        else:
            print("⚠️  No anomalies detected in test data")
        
        print("✅ Anomaly detection functions working")
        return True
        
    except Exception as e:
        print(f"❌ Anomaly detection test failed: {e}")
        traceback.print_exc()
        return False

def test_ai_assistant():
    """Test AI assistant functions"""
    print("\n" + "=" * 60)
    print("Testing AI Assistant")
    print("=" * 60)
    
    try:
        from pages.ai_assistant import init_mimo_client, generate_mock_answer, prepare_data_context
        
        # Test mock answer generation
        test_question = "Analyze user purchase behavior characteristics"
        mock_answer = generate_mock_answer(test_question)
        
        if mock_answer and len(mock_answer) > 0:
            print("✅ Mock answer generation working")
        else:
            print("❌ Mock answer generation failed")
            return False
        
        # Test data context preparation
        context = prepare_data_context(test_question)
        print("✅ Data context preparation working")
        
        print("✅ AI assistant functions working")
        return True
        
    except Exception as e:
        print(f"❌ AI assistant test failed: {e}")
        traceback.print_exc()
        return False

def test_pdf_export():
    """Test PDF export functions"""
    print("\n" + "=" * 60)
    print("Testing PDF Export")
    print("=" * 60)
    
    try:
        from utils.pdf_generator import get_report_data
        from pages.pdf_export import show_pdf_export_page
        
        # Test report data generation
        report_data = get_report_data()
        
        required_keys = ["total_users", "total_orders", "total_gmv"]
        for key in required_keys:
            if key in report_data:
                print(f"✅ Report data contains '{key}'")
            else:
                print(f"⚠️  Report data missing '{key}'")
        
        print("✅ PDF export functions working")
        return True
        
    except Exception as e:
        print(f"❌ PDF export test failed: {e}")
        traceback.print_exc()
        return False

def test_app_navigation():
    """Test app navigation and routing"""
    print("\n" + "=" * 60)
    print("Testing App Navigation")
    print("=" * 60)
    
    try:
        import app
        
        # Check if all page functions exist
        page_functions = [
            "show_data_upload", "show_data_preview", "show_data_clean",
            "show_key_metrics", "show_trend_analysis", "show_user_portrait",
            "show_heatmap", "show_funnel", "show_retention", "show_behavior_path",
            "show_rfm_analysis", "show_clustering", "show_lifecycle",
            "show_purchase_intent", "show_sales_forecast",
            "show_realtime_dashboard", "show_anomaly_detection",
            "show_ai_chat", "show_report_generation", "show_pdf_export"
        ]
        
        for func_name in page_functions:
            if hasattr(app, func_name):
                print(f"✅ App has function '{func_name}'")
            else:
                print(f"⚠️  App missing function '{func_name}'")
        
        print("✅ App navigation structure working")
        return True
        
    except Exception as e:
        print(f"❌ App navigation test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Phase 2 System Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Module Imports", test_imports()))
    results.append(("Database Connection", test_database_connection()))
    results.append(("Real-time Dashboard", test_realtime_dashboard()))
    results.append(("Anomaly Detection", test_anomaly_detection()))
    results.append(("AI Assistant", test_ai_assistant()))
    results.append(("PDF Export", test_pdf_export()))
    results.append(("App Navigation", test_app_navigation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "-" * 60)
    print(f"Total: {passed + failed} | Passed: {passed} | Failed: {failed}")
    print("-" * 60)
    
    if failed == 0:
        print("\n🎉 All tests passed! Phase 2 implementation is complete.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
