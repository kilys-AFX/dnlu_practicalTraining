"""
PDF Export Module - Generate and download PDF reports
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from utils.pdf_generator import generate_pdf_report, get_report_data
from data.database import execute_query
from config.settings import MIMO_CONFIG


def show_pdf_export_page():
    """PDF导出页面"""
    st.markdown("## 📄 PDF报告导出")
    
    st.markdown("基于您的数据生成综合PDF报告。")
    
    # Check dependencies
    check_pdf_dependencies()
    
    # 报告配置
    st.markdown("### ⚙️ 报告设置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_title = st.text_input("报告标题", value="智能零售分析报告")
        
        include_sections = st.multiselect(
            "包含章节",
            ["数据概览", "用户画像", "RFM分析", "行为分析", "AI洞察"],
            default=["数据概览", "RFM分析", "行为分析"]
        )
    
    with col2:
        report_format = st.selectbox(
            "报告格式",
            ["竖版", "横版"]
        )
        
        include_charts = st.checkbox("包含图表", value=True)
    
    # 生成报告
    st.markdown("### 📊 生成报告")
    
    if st.button("🚀 生成PDF报告", type="primary", use_container_width=True):
        with st.spinner("正在生成PDF报告..."):
            try:
                # 获取报告数据
                report_data = get_report_data()
                
                # 添加配置
                report_data["report_title"] = report_title
                report_data["include_sections"] = include_sections
                report_data["report_format"] = report_format
                report_data["include_charts"] = include_charts
                
                # 生成PDF
                output_path = generate_pdf_report(report_data)
                
                st.success(f"✅ 报告生成成功！")
                
                # 提供下载链接
                with open(output_path, "rb") as f:
                    pdf_bytes = f.read()
                
                st.download_button(
                    label="📥 下载PDF报告",
                    data=pdf_bytes,
                    file_name=f"retail_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                # 预览
                st.markdown("### 👁️ 报告预览")
                st.info("浏览器中无法预览PDF，请下载后查看。")
                
            except ImportError as e:
                st.error(f"❌ 缺少依赖：{str(e)}")
                st.markdown("请安装以下依赖之一：")
                st.markdown("- `pip install weasyprint`（推荐）")
                st.markdown("- `pip install reportlab`（备选）")
            
            except Exception as e:
                st.error(f"❌ 报告生成失败：{str(e)}")
    
    # 报告历史
    st.markdown("### 📂 最近报告")
    
    reports_dir = Path("reports")
    if reports_dir.exists():
        pdf_files = list(reports_dir.glob("*.pdf"))
        pdf_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if pdf_files:
            for pdf_file in pdf_files[:5]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(f"{pdf_file.name} ({pdf_file.stat().st_size // 1024} KB)")
                with col2:
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="下载",
                            data=f.read(),
                            file_name=pdf_file.name,
                            mime="application/pdf",
                            key=f"dl_{pdf_file.name}"
                        )
        else:
            st.info("ℹ️ 暂无生成的报告。")
    else:
        st.info("ℹ️ 暂无生成的报告。")


def check_pdf_dependencies():
    """检查PDF生成依赖是否可用"""
    dependencies = []
    
    # Check weasyprint
    try:
        import weasyprint
        dependencies.append("✅ WeasyPrint (HTML → PDF)")
    except ImportError:
        dependencies.append("❌ WeasyPrint 未安装")
    
    # Check reportlab
    try:
        import reportlab
        dependencies.append("✅ ReportLab (纯Python)")
    except ImportError:
        dependencies.append("❌ ReportLab 未安装")
    
    # Display status
    with st.expander("📦 依赖状态", expanded=False):
        for dep in dependencies:
            st.markdown(dep)
        
        if "❌" in "\n".join(dependencies):
            st.markdown("---")
            st.markdown("**安装缺少的依赖：**")
            st.code("pip install weasyprint", language="bash")
            st.caption("或")
            st.code("pip install reportlab", language="bash")


def show_quick_report():
    """快速报告生成（简化版）"""
    st.markdown("### ⚡ 快速报告")
    st.markdown("一键生成基础报告。")
    
    if st.button("⚡ 生成快速报告", use_container_width=True):
        with st.spinner("正在生成快速报告..."):
            try:
                # Get basic data
                report_data = get_report_data()
                
                # Generate PDF
                output_path = generate_pdf_report(report_data)
                
                st.success("✅ 快速报告生成成功！")
                
                # Download
                with open(output_path, "rb") as f:
                    pdf_bytes = f.read()
                
                st.download_button(
                    label="📥 下载快速报告",
                    data=pdf_bytes,
                    file_name=f"quick_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ 快速报告生成失败：{str(e)}")


if __name__ == "__main__":
    show_pdf_export_page()
