"""
数据管理模块 - 上传/预览/清洗
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import tempfile

from data.database import bulk_insert, clear_table, execute_query, table_exists
from utils.data_processor import clean_data


def show_data_upload_page():
    """数据上传页面"""
    st.markdown("## 📤 数据上传")
    
    # 上传方式选择
    upload_method = st.radio(
        "选择上传方式",
        ["上传文件", "生成模拟数据"],
        horizontal=True
    )
    
    if upload_method == "上传文件":
        # 文件上传
        uploaded_file = st.file_uploader(
            "选择文件",
            type=["csv", "xlsx", "xls"],
            help="支持 CSV、Excel 格式"
        )
        
        if uploaded_file is not None:
            try:
                # 读取文件
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ 文件上传成功！共 {len(df)} 行，{len(df.columns)} 列")
                
                # 预览数据
                st.markdown("### 数据预览")
                st.dataframe(df.head(10), use_container_width=True)
                
                # 选择目标表
                table_name = st.selectbox(
                    "选择目标表",
                    ["users", "products", "orders", "order_items", "user_behavior"]
                )
                
                # 确认导入
                if st.button("确认导入数据库", type="primary"):
                    with st.spinner("正在导入数据..."):
                        # 清空原表
                        clear_table(table_name)
                        
                        # 导入新数据
                        success = bulk_insert(table_name, df)
                        
                        if success:
                            st.success(f"✅ 数据已成功导入到 {table_name} 表！")
                        else:
                            st.error("❌ 数据导入失败，请检查数据格式")
                
            except Exception as e:
                st.error(f"❌ 文件读取失败: {str(e)}")
    
    else:  # 生成模拟数据
        st.markdown("### 生成模拟数据")
        st.markdown("根据设置的参数生成模拟零售数据，用于系统测试和演示。")
        
        col1, col2 = st.columns(2)
        
        with col1:
            num_users = st.number_input("用户数量", min_value=100, max_value=10000, value=1000)
            num_products = st.number_input("商品数量", min_value=10, max_value=1000, value=200)
        
        with col2:
            num_orders = st.number_input("订单数量", min_value=100, max_value=50000, value=5000)
            num_behaviors = st.number_input("行为记录数", min_value=1000, max_value=100000, value=50000)
        
        if st.button("🚀 生成模拟数据", type="primary", use_container_width=True):
            with st.spinner("正在生成模拟数据..."):
                from data.data_generator import generate_all_data
                data = generate_all_data(num_users, num_products, num_orders, num_behaviors)
                st.success("✅ 模拟数据生成完成！")
                st.json({k: len(v) for k, v in data.items()})


def show_data_preview_page():
    """数据预览页面"""
    st.markdown("## 👁️ 数据预览")
    
    # 选择表
    tables = ["users", "products", "orders", "order_items", "user_behavior"]
    selected_table = st.selectbox("选择数据表", tables)
    
    if selected_table:
        # 检查表是否存在
        if not table_exists(selected_table):
            st.warning(f"⚠️ 表 {selected_table} 不存在，请先上传数据或生成模拟数据")
            return
        
        # 查询数据
        df = execute_query(f"SELECT * FROM {selected_table}")
        
        if df.empty:
            st.info(f"📭 表 {selected_table} 中没有数据")
            return
        
        # 显示基本信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总记录数", len(df))
        with col2:
            st.metric("字段数", len(df.columns))
        with col3:
            st.metric("缺失值", df.isnull().sum().sum())
        
        # 数据显示选项
        st.markdown("### 数据详情")
        num_rows = st.slider("显示行数", min_value=10, max_value=1000, value=100)
        
        st.dataframe(df.head(num_rows), use_container_width=True)
        
        # 字段信息
        st.markdown("### 字段信息")
        col_info = pd.DataFrame({
            "字段名": df.columns,
            "数据类型": df.dtypes.values,
            "缺失值": df.isnull().sum().values,
            "缺失率": (df.isnull().sum() / len(df) * 100).round(2).values
        })
        st.dataframe(col_info, use_container_width=True)
        
        # 统计信息
        st.markdown("### 统计信息")
        st.dataframe(df.describe(include="all"), use_container_width=True)


def show_data_clean_page():
    """数据清洗页面"""
    st.markdown("## 🧹 数据清洗")
    
    # 选择表
    tables = ["users", "products", "orders", "order_items", "user_behavior"]
    selected_table = st.selectbox("选择数据表", tables)
    
    if selected_table and table_exists(selected_table):
        df = execute_query(f"SELECT * FROM {selected_table}")
        
        if df.empty:
            st.info(f"📭 表 {selected_table} 中没有数据")
            return
        
        # 清洗选项
        st.markdown("### 清洗规则")
        
        col1, col2 = st.columns(2)
        
        with col1:
            drop_duplicates = st.checkbox("去重", value=True)
            fill_missing = st.selectbox(
                "填充缺失值",
                ["不填充", "均值", "中位数", "众数", "删除"]
            )
        
        with col2:
            handle_outliers = st.selectbox(
                "异常值处理",
                ["不处理", "截断", "删除"]
            )
        
        # 预览清洗前
        st.markdown("### 清洗前数据")
        st.dataframe(df.head(10), use_container_width=True)
        
        # 执行清洗
        if st.button("🚀 执行清洗", type="primary"):
            with st.spinner("正在清洗数据..."):
                # 构建清洗规则
                rules = {
                    "drop_duplicates": drop_duplicates,
                    "fill_missing": fill_missing if fill_missing != "不填充" else None,
                    "handle_outliers": handle_outliers if handle_outliers != "不处理" else None
                }
                
                # 执行清洗
                df_cleaned = clean_data(df, rules)
                
                # 预览清洗后
                st.markdown("### 清洗后数据")
                st.dataframe(df_cleaned.head(10), use_container_width=True)
                
                # 对比信息
                st.markdown("### 清洗对比")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("清洗前行数", len(df))
                with col2:
                    st.metric("清洗后行数", len(df_cleaned))
                with col3:
                    st.metric("删除行数", len(df) - len(df_cleaned))
                
                # 保存清洗后的数据
                if st.button("💾 保存清洗结果", type="secondary"):
                    with st.spinner("正在保存..."):
                        clear_table(selected_table)
                        bulk_insert(selected_table, df_cleaned)
                        st.success("✅ 清洗结果已保存到数据库！")


if __name__ == "__main__":
    show_data_upload_page()
