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
    st.markdown("""
    <div class="page-header">
        <h1>数据上传</h1>
        <div class="breadcrumb">首页 / <span>数据管理</span> / 数据上传</div>
    </div>
    """, unsafe_allow_html=True)
    
    upload_method = st.radio("选择上传方式", ["📂 上传文件", "🔄 生成模拟数据"], horizontal=True)
    
    if "上传文件" in upload_method:
        with st.container(border=True):
            st.markdown("### 📂 文件上传")
            uploaded_file = st.file_uploader(
                "拖拽或点击选择文件",
                type=["csv", "xlsx", "xls"],
                help="支持 CSV、Excel (.xlsx/.xls) 格式，最大200MB"
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
                    st.markdown("#### 📋 数据预览")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # 选择目标表
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        table_name = st.selectbox(
                            "选择目标表",
                            ["users", "products", "orders", "order_items", "user_behavior"],
                            format_func=lambda x: {"users": "👥 用户表", "products": "📦 商品表", 
                                                   "orders": "🛒 订单表", "order_items": "📋 订单明细", 
                                                   "user_behavior": "🔍 行为日志"}[x]
                        )
                    
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("📥 确认导入", type="primary", use_container_width=True):
                            with st.spinner("正在导入数据..."):
                                clear_table(table_name)
                                success = bulk_insert(table_name, df)
                                if success:
                                    st.success(f"✅ 数据已成功导入到 {table_name} 表！")
                                else:
                                    st.error("❌ 数据导入失败，请检查数据格式")
                    
                except Exception as e:
                    st.error(f"❌ 文件读取失败: {str(e)}")
    
    else:
        with st.container(border=True):
            st.markdown("### 🔄 生成模拟数据")
            st.markdown("根据参数自动生成符合真实业务场景的模拟零售数据，用于系统测试和演示。")
            
            col1, col2 = st.columns(2)
            
            with col1:
                num_users = st.number_input("👥 用户数量", min_value=100, max_value=10000, value=1000, step=100)
                num_products = st.number_input("📦 商品数量", min_value=10, max_value=1000, value=200, step=10)
            
            with col2:
                num_orders = st.number_input("🛒 订单数量", min_value=100, max_value=50000, value=5000, step=500)
                num_behaviors = st.number_input("🔍 行为记录", min_value=1000, max_value=100000, value=50000, step=1000)
            
            if st.button("🚀 一键生成模拟数据", type="primary", use_container_width=True):
                with st.spinner("正在生成模拟数据..."):
                    from data.data_generator import generate_all_data
                    data = generate_all_data(num_users, num_products, num_orders, num_behaviors)
                    st.success("✅ 模拟数据生成完成！")
                    
                    gen_col1, gen_col2, gen_col3, gen_col4 = st.columns(4)
                    with gen_col1:
                        st.metric("👥 用户", f"{len(data.get('users', []))}")
                    with gen_col2:
                        st.metric("📦 商品", f"{len(data.get('products', []))}")
                    with gen_col3:
                        st.metric("🛒 订单", f"{len(data.get('orders', []))}")
                    with gen_col4:
                        st.metric("🔍 行为", f"{len(data.get('behaviors', []))}")


def show_data_preview_page():
    """数据预览页面"""
    st.markdown("""
    <div class="page-header">
        <h1>数据预览</h1>
        <div class="breadcrumb">首页 / <span>数据管理</span> / 数据预览</div>
    </div>
    """, unsafe_allow_html=True)
    
    tables = ["users", "products", "orders", "order_items", "user_behavior"]
    table_labels = {"users": "👥 用户表", "products": "📦 商品表", "orders": "🛒 订单表",
                   "order_items": "📋 订单明细", "user_behavior": "🔍 行为日志"}
    
    selected_table = st.selectbox(
        "选择数据表",
        tables,
        format_func=lambda x: table_labels.get(x, x)
    )
    
    if selected_table:
        if not table_exists(selected_table):
            st.warning(f"⚠️ 表 {selected_table} 不存在，请先上传数据或生成模拟数据")
            return
        
        df = execute_query(f"SELECT * FROM {selected_table}")
        
        if df.empty:
            st.info(f"📭 表 {selected_table} 中没有数据")
            return
        
        # 基本统计卡片
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("📊 总记录数", f"{len(df):,}")
        with m2:
            st.metric("📋 字段数", len(df.columns))
        with m3:
            st.metric("⚠ 缺失值", df.isnull().sum().sum())
        
        # 数据详情
        with st.container(border=True):
            st.markdown("### 📋 数据详情")
            num_rows = st.slider("显示行数", min_value=10, max_value=1000, value=100)
            st.dataframe(df.head(num_rows), use_container_width=True)
        
        # 字段和统计信息
        tab1, tab2 = st.tabs(["📋 字段信息", "📊 统计信息"])
        
        with tab1:
            col_info = pd.DataFrame({
                "字段名": df.columns,
                "数据类型": df.dtypes.values,
                "缺失值": df.isnull().sum().values,
                "缺失率": (df.isnull().sum() / len(df) * 100).round(2).values
            })
            st.dataframe(col_info, use_container_width=True, hide_index=True)
        
        with tab2:
            st.dataframe(df.describe(include="all"), use_container_width=True)


def show_data_clean_page():
    """数据清洗页面"""
    st.markdown("""
    <div class="page-header">
        <h1>数据清洗</h1>
        <div class="breadcrumb">首页 / <span>数据管理</span> / 数据清洗</div>
    </div>
    """, unsafe_allow_html=True)
    
    tables = ["users", "products", "orders", "order_items", "user_behavior"]
    table_labels = {"users": "👥 用户表", "products": "📦 商品表", "orders": "🛒 订单表",
                   "order_items": "📋 订单明细", "user_behavior": "🔍 行为日志"}
    
    selected_table = st.selectbox(
        "选择要清洗的数据表",
        tables,
        format_func=lambda x: table_labels.get(x, x)
    )
    
    if selected_table and table_exists(selected_table):
        df = execute_query(f"SELECT * FROM {selected_table}")
        
        if df.empty:
            st.info(f"📭 表 {selected_table} 中没有数据")
            return
        
        # 清洗规则
        with st.container(border=True):
            st.markdown("### ⚙️ 清洗规则")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                drop_duplicates = st.checkbox("🗑 去除重复行", value=True)
            with col2:
                fill_missing = st.selectbox("📝 缺失值填充", ["不填充", "均值", "中位数", "众数", "删除"])
            with col3:
                handle_outliers = st.selectbox("🔍 异常值处理", ["不处理", "截断", "删除"])
        
        # 清洗前后对比
        st.markdown("### 📋 数据预览（清洗前）")
        st.dataframe(df.head(10), use_container_width=True)
        
        if st.button("🚀 执行清洗", type="primary", use_container_width=True):
            with st.spinner("正在清洗数据..."):
                rules = {
                    "drop_duplicates": drop_duplicates,
                    "fill_missing": fill_missing if fill_missing != "不填充" else None,
                    "handle_outliers": handle_outliers if handle_outliers != "不处理" else None
                }
                
                df_cleaned = clean_data(df, rules)
                
                st.success("✅ 数据清洗完成！")
                
                # 对比信息
                st.markdown("### 📊 清洗对比")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.metric("清洗前行数", f"{len(df):,}")
                with c2:
                    st.metric("清洗后行数", f"{len(df_cleaned):,}")
                with c3:
                    st.metric("删除行数", f"{len(df) - len(df_cleaned)}")
                with c4:
                    st.metric("缺失值变化", f"{df.isnull().sum().sum()} → {df_cleaned.isnull().sum().sum()}")
                
                st.markdown("### 📋 数据预览（清洗后）")
                st.dataframe(df_cleaned.head(10), use_container_width=True)
                
                if st.button("💾 保存清洗结果到数据库", type="secondary", use_container_width=True):
                    with st.spinner("正在保存..."):
                        clear_table(selected_table)
                        bulk_insert(selected_table, df_cleaned)
                        st.success(f"✅ 清洗结果已保存到 {selected_table} 表！")


if __name__ == "__main__":
    show_data_upload_page()
