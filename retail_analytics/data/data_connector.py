"""
数据集成增强模块 - 支持多种数据源接入
支持：CSV、Excel、JSON、API、数据库等
"""
import pandas as pd
import sqlite3
import requests
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
import streamlit as st
from config.settings import DATABASE_PATH


class DataConnector:
    """数据连接器基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.connection_status = False
        self.error_message = None
    
    def connect(self) -> bool:
        """建立连接"""
        raise NotImplementedError
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            return self.connect()
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def fetch_data(self, query: Any = None) -> Optional[pd.DataFrame]:
        """获取数据"""
        raise NotImplementedError
    
    def get_schema(self) -> Optional[Dict]:
        """获取数据结构信息"""
        raise NotImplementedError


class CSVConnector(DataConnector):
    """CSV文件连接器"""
    
    def __init__(self, file_path: str):
        super().__init__(f"CSV_{Path(file_path).name}")
        self.file_path = file_path
        self.df = None
    
    def connect(self) -> bool:
        try:
            # 尝试不同的编码
            for encoding in ['utf-8', 'gbk', 'gb2312', 'utf-16']:
                try:
                    self.df = pd.read_csv(self.file_path, encoding=encoding)
                    self.connection_status = True
                    return True
                except UnicodeDecodeError:
                    continue
            
            self.error_message = "无法解码文件，请检查文件编码"
            return False
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def fetch_data(self, query: Any = None) -> Optional[pd.DataFrame]:
        if not self.connection_status:
            self.connect()
        
        if self.df is not None:
            if query is not None:
                # 简单的查询过滤
                return self.df.query(query) if isinstance(query, str) else self.df
            return self.df
        return None
    
    def get_schema(self) -> Optional[Dict]:
        if self.df is not None:
            return {
                'columns': list(self.df.columns),
                'dtypes': {col: str(dtype) for col, dtype in self.df.dtypes.items()},
                'shape': self.df.shape,
                'sample': self.df.head(5).to_dict('records')
            }
        return None


class ExcelConnector(DataConnector):
    """Excel文件连接器"""
    
    def __init__(self, file_path: str, sheet_name: Optional[str] = None):
        super().__init__(f"Excel_{Path(file_path).name}")
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.df = None
    
    def connect(self) -> bool:
        try:
            if self.sheet_name:
                self.df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            else:
                # 读取第一个sheet
                self.df = pd.read_excel(self.file_path)
            
            self.connection_status = True
            return True
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def fetch_data(self, query: Any = None) -> Optional[pd.DataFrame]:
        if not self.connection_status:
            self.connect()
        
        if self.df is not None:
            return self.df
        return None
    
    def get_schema(self) -> Optional[Dict]:
        if self.df is not None:
            return {
                'columns': list(self.df.columns),
                'dtypes': {col: str(dtype) for col, dtype in self.df.dtypes.items()},
                'shape': self.df.shape,
                'sheet_name': self.sheet_name or 'Sheet1',
                'sample': self.df.head(5).to_dict('records')
            }
        return None
    
    def get_sheet_names(self) -> List[str]:
        """获取所有sheet名称"""
        try:
            xl = pd.ExcelFile(self.file_path)
            return xl.sheet_names
        except Exception:
            return []


class JSONConnector(DataConnector):
    """JSON文件连接器"""
    
    def __init__(self, file_path: str):
        super().__init__(f"JSON_{Path(file_path).name}")
        self.file_path = file_path
        self.data = None
    
    def connect(self) -> bool:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            self.connection_status = True
            return True
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def fetch_data(self, query: Any = None) -> Optional[pd.DataFrame]:
        if not self.connection_status:
            self.connect()
        
        if self.data is not None:
            # 尝试将JSON转换为DataFrame
            try:
                if isinstance(self.data, list):
                    return pd.DataFrame(self.data)
                elif isinstance(self.data, dict):
                    # 尝试找到包含数据的键
                    for key, value in self.data.items():
                        if isinstance(value, list) and len(value) > 0:
                            return pd.DataFrame(value)
                    # 如果没有找到列表，将整个dict作为一行
                    return pd.DataFrame([self.data])
            except Exception as e:
                self.error_message = f"JSON转DataFrame失败: {str(e)}"
                return None
        
        return None
    
    def get_schema(self) -> Optional[Dict]:
        if self.data is not None:
            if isinstance(self.data, list) and len(self.data) > 0:
                df = pd.DataFrame(self.data)
                return {
                    'type': 'JSON Array',
                    'columns': list(df.columns),
                    'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                    'shape': df.shape,
                    'sample': df.head(5).to_dict('records')
                }
            else:
                return {
                    'type': 'JSON Object',
                    'keys': list(self.data.keys()) if isinstance(self.data, dict) else None,
                    'sample': self.data if len(str(self.data)) < 500 else str(self.data)[:500] + "..."
                }
        return None


class APIConnector(DataConnector):
    """API接口连接器"""
    
    def __init__(self, api_url: str, method: str = 'GET', headers: Optional[Dict] = None, params: Optional[Dict] = None):
        super().__init__(f"API_{api_url.split('/')[-1]}")
        self.api_url = api_url
        self.method = method.upper()
        self.headers = headers or {}
        self.params = params or {}
        self.response_data = None
    
    def connect(self) -> bool:
        try:
            if self.method == 'GET':
                response = requests.get(self.api_url, headers=self.headers, params=self.params, timeout=30)
            elif self.method == 'POST':
                response = requests.post(self.api_url, headers=self.headers, json=self.params, timeout=30)
            else:
                self.error_message = f"不支持的HTTP方法: {self.method}"
                return False
            
            response.raise_for_status()
            self.response_data = response.json()
            self.connection_status = True
            return True
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def fetch_data(self, query: Any = None) -> Optional[pd.DataFrame]:
        if not self.connection_status:
            self.connect()
        
        if self.response_data is not None:
            try:
                # 尝试从API响应中提取数据
                if isinstance(self.response_data, dict):
                    # 常见的API响应格式
                    for key in ['data', 'results', 'items', 'records']:
                        if key in self.response_data and isinstance(self.response_data[key], list):
                            return pd.DataFrame(self.response_data[key])
                    
                    # 如果没有找到标准格式，尝试将整个响应作为一行
                    return pd.DataFrame([self.response_data])
                
                elif isinstance(self.response_data, list):
                    return pd.DataFrame(self.response_data)
                
            except Exception as e:
                self.error_message = f"API数据转DataFrame失败: {str(e)}"
                return None
        
        return None
    
    def get_schema(self) -> Optional[Dict]:
        if self.response_data is not None:
            return {
                'type': 'API Response',
                'response_type': type(self.response_data).__name__,
                'sample': self.response_data if len(str(self.response_data)) < 500 else str(self.response_data)[:500] + "..."
            }
        return None


class DatabaseConnector(DataConnector):
    """数据库连接器（支持SQLite、MySQL、PostgreSQL等）"""
    
    def __init__(self, db_type: str, connection_string: str):
        super().__init__(f"{db_type}_database")
        self.db_type = db_type
        self.connection_string = connection_string
        self.connection = None
    
    def connect(self) -> bool:
        try:
            if self.db_type == 'sqlite':
                self.connection = sqlite3.connect(self.connection_string)
            else:
                # 其他数据库类型需要安装相应的驱动
                self.error_message = f"暂不支持 {self.db_type} 数据库"
                return False
            
            self.connection_status = True
            return True
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def fetch_data(self, query: str) -> Optional[pd.DataFrame]:
        if not self.connection_status:
            self.connect()
        
        if self.connection is not None:
            try:
                return pd.read_sql_query(query, self.connection)
            except Exception as e:
                self.error_message = str(e)
                return None
        
        return None
    
    def get_schema(self) -> Optional[Dict]:
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                schema = {'tables': []}
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    schema['tables'].append({
                        'name': table_name,
                        'columns': [{'name': col[1], 'type': col[2]} for col in columns]
                    })
                
                return schema
            except Exception as e:
                self.error_message = str(e)
                return None
        
        return None
    
    def close(self):
        """关闭数据库连接"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            self.connection_status = False


def create_connector(data_source_type: str, **kwargs) -> Optional[DataConnector]:
    """
    工厂函数：创建数据连接器
    """
    if data_source_type == 'csv':
        file_path = kwargs.get('file_path')
        if file_path:
            return CSVConnector(file_path)
    
    elif data_source_type == 'excel':
        file_path = kwargs.get('file_path')
        sheet_name = kwargs.get('sheet_name')
        if file_path:
            return ExcelConnector(file_path, sheet_name)
    
    elif data_source_type == 'json':
        file_path = kwargs.get('file_path')
        if file_path:
            return JSONConnector(file_path)
    
    elif data_source_type == 'api':
        api_url = kwargs.get('api_url')
        method = kwargs.get('method', 'GET')
        headers = kwargs.get('headers')
        params = kwargs.get('params')
        if api_url:
            return APIConnector(api_url, method, headers, params)
    
    elif data_source_type == 'database':
        db_type = kwargs.get('db_type', 'sqlite')
        connection_string = kwargs.get('connection_string')
        if connection_string:
            return DatabaseConnector(db_type, connection_string)
    
    return None


def save_to_database(df: pd.DataFrame, table_name: str, if_exists: str = 'replace'):
    """
    将数据保存到数据库
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        conn.close()
        return True, f"数据已保存到表 {table_name}"
    except Exception as e:
        return False, f"保存失败: {str(e)}"


if __name__ == "__main__":
    # 测试代码
    print("测试数据连接器...")
    
    # 测试CSV连接器
    csv_connector = CSVConnector("test_data.csv")
    if csv_connector.test_connection():
        print("✅ CSV连接器连接成功")
        df = csv_connector.fetch_data()
        print(f"   数据形状: {df.shape}")
    else:
        print(f"❌ CSV连接器连接失败: {csv_connector.error_message}")
