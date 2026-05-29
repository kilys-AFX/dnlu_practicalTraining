"""
数据集成页面 - 支持多种数据源接入
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import tempfile
import os

from data.data_connector import (
    CSVConnector, 
    ExcelConnector, 
    JSONConnector, 
    APIConnector,
    DatabaseConnector,
    create_connector,
    save_to_database
)
from data.database import execute_query


def show_data_integration_page():
    """数据集成主页面"""
    st.markdown("## 🔗 数据集成增强")
    st.markdown("支持多种数据源接入：CSV、Excel、JSON、API、数据库等")
    
    # 创建标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 CSV文件", 
        "📊 Excel文件", 
        "📋 JSON文件",
        "🌐 API接口",
        "🗄️ 数据库"
    ])
    
    with tab1:
        show_csv_connector()
    
    with tab2:
        show_excel_connector()
    
    with tab3:
        show_json_connector()
    
    with tab4:
        show_api_connector()
    
    with tab5:
        show_database_connector()


def show_csv_connector():
    """CSV文件连接器"""
    st.markdown("### 📄 CSV文件导入")
    
    # 文件上传
    uploaded_file = st.file_uploader("选择CSV文件", type=['csv'], key="csv_uploader")
    
    if uploaded_file is not None:
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # 创建连接器
        connector = CSVConnector(tmp_file_path)
        
        # 测试连接
        if connector.test_connection():
            st.success("✅ CSV文件读取成功！")
            
            # 显示数据预览
            df = connector.fetch_data()
            if df is not None:
                st.markdown("#### 数据预览")
                st.dataframe(df.head(10), use_container_width=True)
                
                # 显示数据结构
                schema = connector.get_schema()
                if schema:
                    with st.expander("数据结构信息"):
                        st.write(f"**列数**: {len(schema['columns'])}")
                        st.write(f"**行数**: {schema['shape'][0]}")
                        st.write("**列信息**:")
                        schema_df = pd.DataFrame({
                            '列名': schema['columns'],
                            '数据类型': [schema['dtypes'][col] for col in schema['columns']]
                        })
                        st.dataframe(schema_df, use_container_width=True)
                
                # 保存到数据库
                st.markdown("#### 保存到数据库")
                table_name = st.text_input("表名", value="imported_csv_data", key="csv_table_name")
                
                if st.button("保存到数据库", key="csv_save_btn"):
                    success, message = save_to_database(df, table_name)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
        else:
            st.error(f"❌ 读取CSV文件失败: {connector.error_message}")
        
        # 清理临时文件
        try:
            os.unlink(tmp_file_path)
        except:
            pass


def show_excel_connector():
    """Excel文件连接器"""
    st.markdown("### 📊 Excel文件导入")
    
    # 文件上传
    uploaded_file = st.file_uploader("选择Excel文件", type=['xlsx', 'xls'], key="excel_uploader")
    
    if uploaded_file is not None:
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # 获取所有sheet名称
        excel_connector = ExcelConnector(tmp_file_path)
        sheet_names = excel_connector.get_sheet_names()
        
        # 选择sheet
        if len(sheet_names) > 1:
            selected_sheet = st.selectbox("选择Sheet", sheet_names, key="excel_sheet_select")
        else:
            selected_sheet = sheet_names[0] if sheet_names else None
        
        # 创建连接器
        connector = ExcelConnector(tmp_file_path, selected_sheet)
        
        # 测试连接
        if connector.test_connection():
            st.success(f"✅ Excel文件读取成功！当前Sheet: {selected_sheet}")
            
            # 显示数据预览
            df = connector.fetch_data()
            if df is not None:
                st.markdown("#### 数据预览")
                st.dataframe(df.head(10), use_container_width=True)
                
                # 显示数据结构
                schema = connector.get_schema()
                if schema:
                    with st.expander("数据结构信息"):
                        st.write(f"**Sheet名**: {schema['sheet_name']}")
                        st.write(f"**列数**: {len(schema['columns'])}")
                        st.write(f"**行数**: {schema['shape'][0]}")
                
                # 保存到数据库
                st.markdown("#### 保存到数据库")
                table_name = st.text_input("表名", value="imported_excel_data", key="excel_table_name")
                
                if st.button("保存到数据库", key="excel_save_btn"):
                    success, message = save_to_database(df, table_name)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
        else:
            st.error(f"❌ 读取Excel文件失败: {connector.error_message}")
        
        # 清理临时文件
        try:
            os.unlink(tmp_file_path)
        except:
            pass


def show_json_connector():
    """JSON文件连接器"""
    st.markdown("### 📋 JSON文件导入")
    
    # 文件上传
    uploaded_file = st.file_uploader("选择JSON文件", type=['json'], key="json_uploader")
    
    if uploaded_file is not None:
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # 创建连接器
        connector = JSONConnector(tmp_file_path)
        
        # 测试连接
        if connector.test_connection():
            st.success("✅ JSON文件读取成功！")
            
            # 显示数据结构
            schema = connector.get_schema()
            if schema:
                with st.expander("JSON结构信息"):
                    st.json(schema['sample'])
            
            # 获取数据
            df = connector.fetch_data()
            if df is not None:
                st.markdown("#### 数据预览")
                st.dataframe(df.head(10), use_container_width=True)
                
                # 保存到数据库
                st.markdown("#### 保存到数据库")
                table_name = st.text_input("表名", value="imported_json_data", key="json_table_name")
                
                if st.button("保存到数据库", key="json_save_btn"):
                    success, message = save_to_database(df, table_name)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
            else:
                st.warning("⚠️ 无法将JSON数据转换为表格格式")
        else:
            st.error(f"❌ 读取JSON文件失败: {connector.error_message}")
        
        # 清理临时文件
        try:
            os.unlink(tmp_file_path)
        except:
            pass


def show_api_connector():
    """API接口连接器"""
    st.markdown("### 🌐 API接口导入")
    
    # API配置
    st.markdown("#### API配置")
    col1, col2 = st.columns(2)
    
    with col1:
        api_url = st.text_input("API URL", value="https://jsonplaceholder.typicode.com/posts", key="api_url")
        method = st.selectbox("HTTP方法", ["GET", "POST"], key="api_method")
    
    with col2:
        headers_str = st.text_area("请求头 (JSON格式)", value='{"Content-Type": "application/json"}', key="api_headers")
        params_str = st.text_area("请求参数 (JSON格式)", value='{}', key="api_params")
    
    # 解析JSON
    try:
        headers = json.loads(headers_str) if headers_str else {}
        params = json.loads(params_str) if params_str else {}
    except json.JSONDecodeError as e:
        st.error(f"❌ JSON格式错误: {str(e)}")
        return
    
    # 测试连接
    if st.button("测试API连接", key="api_test_btn"):
        connector = APIConnector(api_url, method, headers, params)
        
        if connector.test_connection():
            st.success("✅ API连接成功！")
            
            # 显示响应数据
            df = connector.fetch_data()
            if df is not None:
                st.markdown("#### 数据预览")
                st.dataframe(df.head(10), use_container_width=True)
                
                # 保存到数据库
                st.markdown("#### 保存到数据库")
                table_name = st.text_input("表名", value="imported_api_data", key="api_table_name")
                
                if st.button("保存到数据库", key="api_save_btn"):
                    success, message = save_to_database(df, table_name)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
            else:
                st.warning("⚠️ 无法将API响应转换为表格格式")
                with st.expander("查看原始响应"):
                    st.json(connector.response_data)
        else:
            st.error(f"❌ API连接失败: {connector.error_message}")


def show_database_connector():
    """数据库连接器"""
    st.markdown("### 🗄️ 数据库导入")
    
    # 数据库配置
    st.markdown("#### 数据库配置")
    db_type = st.selectbox("数据库类型", ["SQLite", "MySQL", "PostgreSQL"], key="db_type")
    
    if db_type == "SQLite":
        db_path = st.text_input("数据库文件路径", value=str(Path(__file__).parent.parent / "data" / "retail_analytics.db"), key="db_path")
        connection_string = db_path
    else:
        st.warning(f"⚠️ {db_type} 数据库支持正在开发中...")
        return
    
    # 连接数据库
    if st.button("连接数据库", key="db_connect_btn"):
        connector = DatabaseConnector(db_type.lower(), connection_string)
        
        if connector.test_connection():
            st.success(f"✅ {db_type}数据库连接成功！")
            
            # 显示数据库结构
            schema = connector.get_schema()
            if schema and 'tables' in schema:
                st.markdown("#### 数据库结构")
                for table in schema['tables']:
                    with st.expander(f"表: {table['name']}"):
                        columns_df = pd.DataFrame(table['columns'])
                        st.dataframe(columns_df, use_container_width=True)
            
            # 执行SQL查询
            st.markdown("#### 执行SQL查询")
            sql_query = st.text_area("SQL查询语句", value="SELECT * FROM users LIMIT 10", key="db_sql_query")
            
            if st.button("执行查询", key="db_execute_btn"):
                try:
                    df = connector.fetch_data(sql_query)
                    if df is not None:
                        st.markdown("#### 查询结果")
                        st.dataframe(df, use_container_width=True)
                        
                        # 保存到当前数据库
                        st.markdown("#### 保存到当前数据库")
                        table_name = st.text_input("表名", value="imported_query_result", key="db_table_name")
                        if_exists = st.selectbox("如果表存在", ["replace", "append", "fail"], key="db_if_exists")
                        
                        if st.button("保存到数据库", key="db_save_btn"):
                            success, message = save_to_database(df, table_name, if_exists)
                            if success:
                                st.success(f"✅ {message}")
                            else:
                                st.error(f"❌ {message}")
                    else:
                        st.warning("⚠️ 查询未返回数据")
                except Exception as e:
                    st.error(f"❌ 查询执行失败: {str(e)}")
            
            # 关闭连接
            connector.close()
        else:
            st.error(f"❌ 数据库连接失败: {connector.error_message}")


if __name__ == "__main__":
    # 测试代码
    show_data_integration_page()