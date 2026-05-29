"""
用户认证和权限管理模块
"""
import streamlit as st
import hashlib
import sqlite3
import secrets
from datetime import datetime, timedelta
from pathlib import Path

# 数据库路径
DB_PATH = Path(__file__).parent.parent / "data" / "retail_analytics.db"

def init_auth_db():
    """初始化认证数据库表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    """)
    
    # 创建会话表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # 创建默认管理员账号
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        admin_password = hash_password('admin123')
        cursor.execute("""
            INSERT INTO users (username, password_hash, email, role)
            VALUES ('admin', ?, 'admin@retail.com', 'admin')
        """, (admin_password,))
    
    conn.commit()
    conn.close()

def hash_password(password):
    """密码哈希"""
    salt = "retail_analytics_salt"  # 在实际应用中应使用随机盐
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def verify_password(password, password_hash):
    """验证密码"""
    return hash_password(password) == password_hash

def authenticate_user(username, password):
    """用户认证"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, password_hash, role, is_active FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[3]:  # 检查账号是否激活
        if verify_password(password, user[1]):
            return {'id': user[0], 'username': username, 'role': user[2]}
    return None

def create_user(username, password, email='', role='user'):
    """创建新用户"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, password_hash, email, role)
            VALUES (?, ?, ?, ?)
        """, (username, password_hash, email, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_id(user_id):
    """根据ID获取用户信息"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, email, role, created_at, last_login, is_active FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'role': user[3],
            'created_at': user[4],
            'last_login': user[5],
            'is_active': user[6]
        }
    return None

def update_last_login(user_id):
    """更新最后登录时间"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def check_permission(user_role, required_role):
    """检查权限"""
    role_hierarchy = {'admin': 3, 'manager': 2, 'user': 1}
    return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)
