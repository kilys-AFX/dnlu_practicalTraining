"""
测试脚本 v2 - 验证中文界面修复和功能修复
"""
import streamlit as st
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

st.markdown("# 🧪 中文化修复验证测试 v2")
st.markdown("此脚本将验证所有页面的中文界面和功能修复。")

# 测试项目
tests = {
    "✅ 主程序 (app.py)": [
        "侧边栏菜单中文",
        "首页内容中文",
        "按钮文字中文"
    ],
    "✅ RFM分析 (user_profiling.py)": [
        "SQL查询条件正确（Cancelled）",
        "页面标题中文",
        "图表标签中文"
    ],
    "✅ 实时数据大屏 (realtime_dashboard.py)": [
        "订单状态中文显示",
        "状态映射正确",
        "页面标题中文"
    ],
    "✅ 异常检测 (anomaly_detection.py)": [
        "异常类型中文（GMV异常、订单数异常）",
        "严重程度中文（高、中）",
        "按钮文字中文",
        "图表标签中文",
        "空数据返回DataFrame"
    ],
    "✅ PDF导出 (pdf_export.py)": [
        "依赖检查中文",
        "按钮文字中文",
        "配置导入正确（MIMO_CONFIG）"
    ],
    "✅ 数据概览 (data_overview.py)": [
        "SQL查询条件正确（Cancelled）",
        "页面标题中文",
        "指标标签中文"
    ],
    "✅ 预测模型 (prediction_models.py)": [
        "页面标题中文",
        "按钮文字中文",
        "输入框标签中文",
        "图表标签中文"
    ],
    "✅ AI助手 (ai_assistant.py)": [
        "页面标题中文",
        "快速问题中文",
        "按钮文字中文",
        "模拟回答中文"
    ]
}

# 显示测试项目
st.markdown("## 📋 测试项目列表")
for module, test_items in tests.items():
    with st.expander(module, expanded=True):
        for item in test_items:
            st.markdown(f"- [ ] {item}")

# 手动测试指南
st.markdown("## 📝 手动测试指南")
st.markdown("""
1. **启动系统**：
   - 双击运行 `启动测试.bat`
   - 或手动执行：`streamlit run app.py`

2. **逐一检查页面**：
   - 点击侧边栏的每个菜单项
   - 确认页面标题、按钮、标签都是中文
   - 测试主要功能是否正常工作

3. **重点测试之前的错误页面**：
   - **RFM分析**：应能正常显示分析结果
   - **实时数据大屏**：订单状态应显示中文
   - **异常检测**：应能正常检测异常
   - **PDF导出**：应能正常生成报告

4. **如果发现问题**：
   - 记录哪个页面还有英文
   - 记录哪个功能还有错误
   - 提供错误信息或截图
""")

# 快速启动按钮
st.markdown("## 💡 快速启动")
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 启动系统", use_container_width=True, type="primary"):
        import subprocess
        import webbrowser
        import time
        
        # 启动streamlit
        process = subprocess.Popen(
            ["streamlit", "run", "app.py", "--server.headless", "true"],
            cwd=str(Path(__file__).parent)
        )
        
        # 等待启动
        time.sleep(3)
        
        # 打开浏览器
        webbrowser.open("http://localhost:8501")
        
        st.success("✅ 系统已启动！请在浏览器中查看。")

with col2:
    if st.button("📖 查看修复总结", use_container_width=True):
        import os
        os.startfile("修复总结.md")

# 配置文件检查
st.markdown("## ⚙️ 配置文件检查")
try:
    from config.settings import APP_CONFIG, MIMO_CONFIG, MODEL_CONFIG
    
    st.markdown("### APP_CONFIG")
    st.json(APP_CONFIG)
    
    st.markdown("### MIMO_CONFIG")
    st.json({k: v if k != "api_key" else "***" for k, v in MIMO_CONFIG.items()})
    
    st.markdown("### MODEL_CONFIG")
    st.json({k: str(v) for k, v in MODEL_CONFIG.items()})
    
except Exception as e:
    st.error(f"❌ 配置文件加载失败: {str(e)}")

# 数据库检查
st.markdown("## 🗄️ 数据库检查")
try:
    from data.database import execute_query
    
    # 检查表是否存在
    tables = ["users", "products", "orders", "order_items", "user_behavior"]
    
    for table in tables:
        count = execute_query(f"SELECT COUNT(*) as count FROM {table}").iloc[0]["count"]
        st.markdown(f"- **{table}**: {count:,} 条记录")
    
    # 检查订单状态值
    st.markdown("### 订单状态值")
    status_dist = execute_query("SELECT status, COUNT(*) as count FROM orders GROUP BY status")
    st.dataframe(status_dist, use_container_width=True)
    
    # 检查是否有中文状态值（应该是英文）
    has_chinese = status_dist[status_dist["status"].str.contains("取消|支付|发货|完成", na=False)]
    if not has_chinese.empty:
        st.warning("⚠️ 检测到中文状态值，请确认是否正确")
    else:
        st.success("✅ 订单状态值都是英文（符合预期）")
    
except Exception as e:
    st.error(f"❌ 数据库检查失败: {str(e)}")

# 文件编码检查
st.markdown("## 📄 文件编码检查")
import os

pages_dir = Path(__file__).parent / "pages"
if pages_dir.exists():
    py_files = list(pages_dir.glob("*.py"))
    
    st.markdown(f"### 找到 {len(py_files)} 个Python文件")
    
    for py_file in py_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 检查是否包含中文字符
            has_chinese = any('\u4e00' <= c <= '\u9fff' for c in content)
            
            if has_chinese:
                st.markdown(f"- ✅ {py_file.name}: 包含中文")
            else:
                st.markdown(f"- ⚠️ {py_file.name}: 未检测到中文")
        
        except Exception as e:
            st.markdown(f"- ❌ {py_file.name}: 读取失败 - {str(e)}")

st.markdown("---")
st.markdown("### 📞 需要帮助？")
st.markdown("如果测试中发现问题，请提供：")
st.markdown("1. 具体的错误信息或截图")
st.markdown("2. 哪个页面还有英文")
st.markdown("3. 哪个功能还有错误")
