"""
系统测试脚本 - 检查所有模块是否能正常导入
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("智能零售用户行为分析系统 - 模块测试")
print("=" * 60)

# 测试计数器
passed = 0
failed = 0

def test_module(module_name, display_name):
    """测试模块导入"""
    global passed, failed
    try:
        __import__(module_name)
        print(f"  ✓ {display_name:20s} - 导入成功")
        passed += 1
        return True
    except Exception as e:
        print(f"  ✗ {display_name:20s} - 导入失败: {e}")
        failed += 1
        return False

# 测试 1: 配置文件
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
    ("pages.data_management", "数据管理"),
    ("pages.data_overview", "数据概览"),
    ("pages.behavior_analysis", "行为分析"),
    ("pages.user_profiling", "用户画像"),
    ("pages.prediction_models", "预测模型"),
    ("pages.realtime_dashboard", "实时监控"),
    ("pages.anomaly_detection", "异常检测"),
    ("pages.ai_assistant", "AI助手"),
    ("pages.pdf_export", "PDF导出"),
]

for module_name, display_name in pages:
    test_module(module_name, display_name)

# 测试 6: 主程序
print("\n[6] 测试主程序...")
test_module("app", "主程序")

# 总结
print("\n" + "=" * 60)
print(f"测试总结: 成功 {passed} 个, 失败 {failed} 个")
print("=" * 60)

if failed == 0:
    print("\n✅ 所有模块测试通过！系统可以正常运行。")
    print("\n启动方法:")
    print("  1. 打开 CMD 命令行")
    print("  2. 切换到项目目录: cd /d d:\\codebuddy\\education\\retail_analytics")
    print("  3. 激活 Conda 环境: conda activate retail-analytics")
    print("  4. 启动系统: streamlit run app.py")
    print("  5. 在浏览器中访问: http://localhost:8501")
else:
    print(f"\n⚠️  有 {failed} 个模块存在问题，请检查错误信息。")

print("\n" + "=" * 60)
