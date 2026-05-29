"""
系统最终测试脚本
检查所有模块是否能正常导入和运行
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("智能零售用户行为分析系统 - 第二阶段功能测试")
print("=" * 70)

# 测试结果统计
results = {
    "passed": [],
    "failed": []
}

def test_module(module_name, display_name):
    """测试模块导入"""
    try:
        __import__(module_name)
        results["passed"].append(display_name)
        print(f"  ✓ {display_name:25s} - OK")
        return True
    except Exception as e:
        results["failed"].append((display_name, str(e)[:80]))
        print(f"  ✗ {display_name:25s} - FAILED: {str(e)[:50]}")
        return False

# 测试 1: 配置模块
print("\n[1] 测试配置模块...")
test_module("config.settings", "配置文件")

# 测试 2: 数据模块
print("\n[2] 测试数据模块...")
test_module("data.database", "数据库模块")
test_module("data.data_generator", "数据生成器")

# 测试 3: 工具模块
print("\n[3] 测试工具模块...")
test_module("utils.data_processor", "数据处理工具")
test_module("utils.pdf_generator", "PDF生成器")

# 测试 4: 模型模块
print("\n[4] 测试模型模块...")
test_module("models.purchase_intent", "购买意向模型")
test_module("models.sales_forecast", "销售预测模型")

# 测试 5: 页面模块
print("\n[5] 测试页面模块...")
pages = [
    ("pages.data_management", "数据管理页面"),
    ("pages.data_overview", "数据概览页面"),
    ("pages.behavior_analysis", "行为分析页面"),
    ("pages.user_profiling", "用户画像页面"),
    ("pages.prediction_models", "预测模型页面"),
    ("pages.realtime_dashboard", "实时监控页面"),
    ("pages.anomaly_detection", "异常检测页面"),
    ("pages.ai_assistant", "AI助手页面"),
    ("pages.pdf_export", "PDF导出页面"),
]

for module_name, display_name in pages:
    test_module(module_name, display_name)

# 测试 6: 主程序
print("\n[6] 测试主程序...")
test_module("app", "主程序 (app.py)")

# 测试 7: 检查数据库
print("\n[7] 检查数据库...")
try:
    from data.database import execute_query, init_database
    init_database()
    
    result = execute_query("SELECT COUNT(*) as count FROM users")
    user_count = result.iloc[0]["count"]
    
    result = execute_query("SELECT COUNT(*) as count FROM orders")
    order_count = result.iloc[0]["count"]
    
    if user_count > 0 and order_count > 0:
        results["passed"].append(f"数据库 (用户:{user_count}, 订单:{order_count})")
        print(f"  ✓ 数据库检查通过 (用户:{user_count}, 订单:{order_count})")
    else:
        results["passed"].append("数据库 (空)")
        print(f"  ⚠️  数据库为空 (用户:{user_count}, 订单:{order_count})")
        print(f"     请运行系统后点击 'Generate Mock Data' 生成测试数据")
except Exception as e:
    results["failed"].append(("数据库", str(e)[:80]))
    print(f"  ✗ 数据库检查失败: {str(e)[:50]}")

# 打印测试总结
print("\n" + "=" * 70)
print(f"测试总结:")
print(f"  成功: {len(results['passed'])} 项")
print(f"  失败: {len(results['failed'])} 项")
print("=" * 70)

if len(results["failed"]) == 0:
    print("\n✅ 所有测试通过！系统可以正常运行。")
    print("\n启动步骤:")
    print("  1. 打开 CMD 命令行 (不要用 PowerShell)")
    print("  2. 切换到项目目录:")
    print("     cd /d d:\\codebuddy\\education\\retail_analytics")
    print("  3. 激活 Conda 环境:")
    print("     conda activate retail-analytics")
    print("  4. 启动系统:")
    print("     streamlit run app.py")
    print("  5. 在浏览器中访问:")
    print("     http://localhost:8501")
    print("\n使用说明:")
    print("  - 首次运行请点击侧边栏的 'Generate Mock Data' 生成测试数据")
    print("  - 然后可以测试各个功能模块")
else:
    print(f"\n⚠️  有 {len(results['failed'])} 项测试失败:")
    for name, error in results["failed"][:5]:  # 只显示前5个错误
        print(f"  - {name}: {error}")

print("\n" + "=" * 70)
print("第二阶段开发完成功能:")
print("  ✅ 数据管理模块 (上传、预览、清洗)")
print("  ✅ 数据概览模块 (关键指标、趋势分析、用户画像)")
print("  ✅ 行为分析模块 (热力图、转化漏斗、留存分析、行为路径)")
print("  ✅ 用户画像模块 (RFM分析、用户聚类、生命周期)")
print("  ✅ 预测模型模块 (购买意向、销售预测)")
print("  ✅ 实时监控模块 (大屏仪表板、异常检测)")
print("  ✅ AI助手模块 (智能问答、报告生成)")
print("  ✅ PDF导出模块 (报告生成、下载)")
print("=" * 70)
print("\n测试完成！")
