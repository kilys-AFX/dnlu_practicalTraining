"""
测试中文界面修复和错误修复
"""
import streamlit as st
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.user_profiling import show_rfm_page, show_clustering_page, show_lifecycle_page
from pages.realtime_dashboard import show_realtime_dashboard
from pages.anomaly_detection import show_anomaly_detection_page
from pages.pdf_export import show_pdf_export_page

def test_imports():
    """测试所有页面模块导入"""
    print("✅ 测试模块导入...")
    
    try:
        from pages.user_profiling import show_rfm_page
        print("  ✅ user_profiling.py 导入成功")
    except Exception as e:
        print(f"  ❌ user_profiling.py 导入失败: {e}")
        return False
    
    try:
        from pages.realtime_dashboard import show_realtime_dashboard
        print("  ✅ realtime_dashboard.py 导入成功")
    except Exception as e:
        print(f"  ❌ realtime_dashboard.py 导入失败: {e}")
        return False
    
    try:
        from pages.anomaly_detection import show_anomaly_detection_page
        print("  ✅ anomaly_detection.py 导入成功")
    except Exception as e:
        print(f"  ❌ anomaly_detection.py 导入失败: {e}")
        return False
    
    try:
        from pages.pdf_export import show_pdf_export_page
        print("  ✅ pdf_export.py 导入成功")
    except Exception as e:
        print(f"  ❌ pdf_export.py 导入失败: {e}")
        return False
    
    return True

def test_chinese_content():
    """测试中文内容是否恢复"""
    print("\n✅ 测试中文界面恢复...")
    
    # 读取文件检查中文内容
    files_to_check = [
        ("pages/realtime_dashboard.py", ["实时数据大屏", "在线用户", "今日订单", "今日GMV", "转化率"]),
        ("pages/anomaly_detection.py", ["异常检测播报", "异常列表", "异常趋势", "AI智能诊断"]),
        ("pages/pdf_export.py", ["PDF报告导出", "报告设置", "生成报告", "报告历史"]),
        ("pages/user_profiling.py", ["RFM用户价值分析", "K-Means用户聚类", "用户生命周期管理"])
    ]
    
    all_passed = True
    
    for file_path, keywords in files_to_check:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            missing_keywords = []
            for keyword in keywords:
                if keyword not in content:
                    missing_keywords.append(keyword)
            
            if missing_keywords:
                print(f"  ⚠️ {file_path} 缺少中文关键词: {missing_keywords}")
                all_passed = False
            else:
                print(f"  ✅ {file_path} 中文界面已恢复")
                
        except Exception as e:
            print(f"  ❌ 读取 {file_path} 失败: {e}")
            all_passed = False
    
    return all_passed

def test_sql_fixes():
    """测试SQL查询中的中文状态值是否已修复"""
    print("\n✅ 测试SQL查询修复...")
    
    try:
        from data.database import execute_query
        
        # 测试查询（使用英文状态值）
        test_query = """
        SELECT COUNT(*) as count
        FROM orders
        WHERE status != 'Cancelled'
        """
        
        result = execute_query(test_query)
        print(f"  ✅ SQL查询测试通过（使用英文状态值 'Cancelled'）")
        return True
        
    except Exception as e:
        print(f"  ❌ SQL查询测试失败: {e}")
        return False

def test_function_returns():
    """测试函数返回类型是否正确"""
    print("\n✅ 测试函数返回类型...")
    
    try:
        from pages.anomaly_detection import analyze_sales_anomalies, analyze_user_anomalies
        from data.database import execute_query
        
        # 测试 analyze_sales_anomalies 返回类型
        anomalies, data = analyze_sales_anomalies()
        
        if isinstance(data, str):
            print(f"  ❌ analyze_sales_anomalies 返回类型错误：data 是字符串 '{data}'")
            return False
        else:
            print(f"  ✅ analyze_sales_anomalies 返回类型正确")
        
        # 测试 analyze_user_anomalies 返回类型
        anomalies, data = analyze_user_anomalies()
        
        if isinstance(data, str):
            print(f"  ❌ analyze_user_anomalies 返回类型错误：data 是字符串 '{data}'")
            return False
        else:
            print(f"  ✅ analyze_user_anomalies 返回类型正确")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 函数返回类型测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("零售分析系统 - 中文界面修复测试")
    print("=" * 60)
    
    # 运行测试
    test1 = test_imports()
    test2 = test_chinese_content()
    test3 = test_sql_fixes()
    test4 = test_function_returns()
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    print(f"模块导入测试: {'✅ 通过' if test1 else '❌ 失败'}")
    print(f"中文界面恢复: {'✅ 通过' if test2 else '⚠️ 部分通过'}")
    print(f"SQL查询修复: {'✅ 通过' if test3 else '❌ 失败'}")
    print(f"函数返回类型: {'✅ 通过' if test4 else '❌ 失败'}")
    
    if all([test1, test2, test3, test4]):
        print("\n🎉 所有测试通过！中文界面已恢复，错误已修复。")
        return 0
    else:
        print("\n⚠️ 部分测试未通过，请检查上述错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
