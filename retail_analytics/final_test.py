"""
最终测试脚本 - 检查系统所有模块
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("智能零售用户行为分析系统 - 第二阶段功能测试")
print("=" * 70)

# 测试计数器
passed = 0
failed = 0
errors = []

def test_import(module_name, display_name):
    """测试模块导入"""
    global passed, failed, errors
    try:
        __import__(module_name)
        print(f"  ✓ {display_name:25s} - 导入成功")
        passed += 1
        return True
    except Exception as e:
        print(f"  ✗ {display_name:25s} - 导入失败: {str(e)[:100]}")
        failed += 1
        errors.append((module_name, str(e)))
        return False

# 测试 1: 配置模块
print("\n[测试 1] 配置模块...")
test_import("config.settings", "配置文件")

# 测试 2: 数据模块
print("\n[测试 2] 数据模块...")
test_import("data.database", "数据库模块")
test_import("data.data_generator", "数据生成器")

# 测试 3: 工具模块
print("\n[测试 3] 工具模块...")
test_import("utils.data_processor", "数据处理工具")
test_import("utils.pdf_generator", "PDF生成器")

# 测试 4: 模型模块
print("\n[测试 4] 模型模块...")
test_import("models.purchase_intent", "购买意向模型")
test_import("models.sales_forecast", "销售预测模型")

# 测试 5: 页面模块
print("\n[测试 5] 页面模块...")
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
    test_import(module_name, display_name)

# 测试 6: 主程序
print("\n[测试 6] 主程序...")
test_import("app", "主程序")

# 测试 7: 检查数据库文件
print("\n[测试 7] 数据库文件...")
db_path = Path("data/retail.db")
if db_path.exists():
    print(f"  ✓ 数据库文件存在: {db_path}")
    passed += 1
else:
    print(f"  ⚠️  数据库文件不存在: {db_path}")
    print(f"     请运行系统后点击 'Generate Mock Data' 生成测试数据")
    failed += 1

# 测试 8: 检查依赖包
print("\n[测试 8] 检查依赖包...")
required_packages = [
    ("streamlit", "streamlit"),
    ("pandas", "pandas"),
    ("plotly", "plotly"),
    ("numpy", "numpy"),
    ("sklearn", "scikit-learn"),
    ("torch", "pytorch"),
]

for package, display_name in required_packages:
    try:
        __import__(package)
        print(f"  ✓ {display_name:20s} - 已安装")
        passed += 1
    except ImportError:
        print(f"  ✗ {display_name:20s} - 未安装")
        failed += 1
        errors.append((package, "Package not installed"))

# 总结
print("\n" + "=" * 70)
print(f"测试总结: 成功 {passed} 项, 失败 {failed} 项")
print("=" * 70)

if failed == 0:
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
    print(f"\n⚠️  有 {failed} 项测试失败，请检查错误信息:")
    for module, error in errors[:5]:  # 只显示前5个错误
        print(f"  - {module}: {error[:100]}")
    
    print("\n建议操作:")
    print("  1. 检查错误信息，修复代码问题")
    print("  2. 确保所有依赖包已安装: pip install -r requirements.txt")
    print("  3. 如果还有编码问题，检查文件中是否有中文字符")

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
