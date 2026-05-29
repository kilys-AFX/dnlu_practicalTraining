"""
数据库初始化和管理 - 支持 SQLite 和 MySQL
"""
import sqlite3
import pymysql
import pandas as pd
from pathlib import Path
from config.settings import DATABASE_PATH, MYSQL_CONFIG, DB_TYPE


def get_connection():
    """获取数据库连接（根据配置自动选择 SQLite 或 MySQL）"""
    if DB_TYPE == "mysql":
        # MySQL 连接
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"],
            charset=MYSQL_CONFIG["charset"],
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    else:
        # SQLite 连接
        conn = sqlite3.connect(DATABASE_PATH)
        return conn


def execute_query(query, params=None):
    """执行查询并返回 DataFrame"""
    # 将 SQLite 语法转换为 MySQL 语法
    if DB_TYPE == "mysql":
        query = query.replace("DATETIME", "DATETIME")
        query = query.replace("AUTOINCREMENT", "AUTO_INCREMENT")
    
    conn = get_connection()
    try:
        if DB_TYPE == "mysql":
            # MySQL 需要设置索引
            return pd.read_sql_query(query, conn, params=params)
        else:
            return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()


def execute_sql(sql, params=None):
    """执行 SQL 语句（INSERT/UPDATE/DELETE）"""
    # 将 SQLite 语法转换为 MySQL 语法
    if DB_TYPE == "mysql":
        sql = sql.replace("AUTOINCREMENT", "AUTO_INCREMENT")
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        
        # 获取最后插入的 ID
        if DB_TYPE == "mysql":
            return cursor.lastrowid
        else:
            return cursor.lastrowid
    finally:
        conn.close()


def bulk_insert(table_name, df):
    """批量插入数据"""
    conn = get_connection()
    try:
        if DB_TYPE == "mysql":
            # MySQL 批量插入
            df.to_sql(table_name, conn, if_exists='append', index=False, method='multi')
        else:
            # SQLite 批量插入
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
        if DB_TYPE == "mysql":
            cursor.execute(f"TRUNCATE TABLE {table_name}")
        else:
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
        if DB_TYPE == "mysql":
            cursor.execute(f"DESCRIBE {table_name}")
        else:
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
        if DB_TYPE == "mysql":
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        else:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
        return cursor.fetchone() is not None
    finally:
        conn.close()


def init_database():
    """初始化数据库，创建所有表（支持 SQLite 和 MySQL）"""
    if DB_TYPE == "mysql":
        init_mysql_database()
    else:
        init_sqlite_database()


def init_sqlite_database():
    """初始化 SQLite 数据库"""
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
        behavior_type TEXT,
        behavior_time DATETIME,
        duration INTEGER,
        device TEXT,
        channel TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """)
    
    conn.commit()
    conn.close()
    print("[OK] SQLite database initialized successfully")


def init_mysql_database():
    """初始化 MySQL 数据库"""
    try:
        # 创建数据库连接
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            charset=MYSQL_CONFIG["charset"]
        )
        cursor = conn.cursor()
        
        # 创建数据库（如果不存在）
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {MYSQL_CONFIG['database']}")
        
        # 用户表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY,
            gender VARCHAR(10),
            age INT,
            city VARCHAR(50),
            register_date DATE,
            last_login DATE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # 商品表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT PRIMARY KEY,
            product_name VARCHAR(200),
            category VARCHAR(50),
            price DECIMAL(10,2),
            stock INT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # 订单表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            order_date DATETIME,
            total_amount DECIMAL(10,2),
            status VARCHAR(20),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # 订单明细表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT,
            product_id INT,
            quantity INT,
            price DECIMAL(10,2),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # 用户行为日志表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_behavior (
            behavior_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            product_id INT,
            behavior_type VARCHAR(20),
            behavior_time DATETIME,
            duration INT,
            device VARCHAR(20),
            channel VARCHAR(20),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        conn.commit()
        conn.close()
        print("[OK] MySQL database initialized successfully")
        
    except Exception as e:
        print(f"[FAIL] MySQL database initialization failed: {e}")
        print("Please check your MySQL configuration in config/settings.py")


if __name__ == "__main__":
    init_database()
