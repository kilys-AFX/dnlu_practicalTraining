"""
数据库初始化和管理
"""
import sqlite3
import pandas as pd
from pathlib import Path
from config.settings import DATABASE_PATH


def init_database():
    """初始化数据库，创建所有表"""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 用户表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        gender TEXT,
        age INTEGER,
        city TEXT,
        register_date DATE,
        last_login DATE
    )
    """)
    
    # 商品表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL,
        stock INTEGER
    )
    """)
    
    # 订单表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        order_date DATETIME,
        total_amount REAL,
        status TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)
    
    # 订单明细表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """)
    
    # 用户行为日志表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_behavior (
        behavior_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        behavior_type TEXT,  -- 浏览/加购/收藏/下单/支付
        behavior_time DATETIME,
        duration INTEGER,  -- 停留时长（秒）
        device TEXT,  -- 设备类型
        channel TEXT,  -- 来源渠道
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """)
    
    conn.commit()
    conn.close()
    print("[OK] Database initialized successfully")


def get_connection():
    """获取数据库连接"""
    return sqlite3.connect(DATABASE_PATH)


def execute_query(query, params=None):
    """执行查询并返回 DataFrame"""
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    finally:
        conn.close()


def execute_sql(sql, params=None):
    """执行 SQL 语句（INSERT/UPDATE/DELETE）"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def bulk_insert(table_name, df):
    """批量插入数据"""
    conn = get_connection()
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()
        return True
    except Exception as e:
        print(f"[FAIL] Bulk insert failed: {e}")
        return False
    finally:
        conn.close()


def clear_table(table_name):
    """清空表数据"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()
        return True
    except Exception as e:
        print(f"[FAIL] Clear table failed: {e}")
        return False
    finally:
        conn.close()


def get_table_info(table_name):
    """获取表结构信息"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        return columns
    finally:
        conn.close()


def table_exists(table_name):
    """检查表是否存在"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()
