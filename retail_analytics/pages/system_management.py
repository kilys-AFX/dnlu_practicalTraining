"""
系统管理页面
"""
import streamlit as st
import sqlite3
from pathlib import Path
from utils.auth import get_user_by_id, check_permission

# 数据库路径
DB_PATH = Path(__file__).parent.parent / "data" / "retail_analytics.db"

def show_user_management_page():
    """用户管理页面（供app.py调用）"""
    st.markdown("## 用户管理")
    
    # 获取所有用户
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role, created_at, last_login, is_active FROM users")
    users = cursor.fetchall()
    conn.close()
    
    if not users:
        st.info("暂无用户数据")
        return
    
    # 显示用户列表
    for user in users:
        with st.expander(f"用户: {user[1]} (角色: {user[3]})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**用户ID**: {user[0]}")
                st.write(f"**邮箱**: {user[2]}")
                st.write(f"**注册时间**: {user[4]}")
            
            with col2:
                st.write(f"**最后登录**: {user[5]}")
                st.write(f"**状态**: {'活跃' if user[6] else '禁用'}")
                
                # 操作按钮
                if st.button(f"切换状态##{user[0]}", key=f"toggle_{user[0]}"):
                    toggle_user_status(user[0])
                
                if st.button(f"删除用户##{user[0]}", key=f"delete_{user[0]}"):
                    delete_user(user[0])

def toggle_user_status(user_id):
    """切换用户状态"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT is_active FROM users WHERE id = ?", (user_id,))
    current_status = cursor.fetchone()[0]
    new_status = 0 if current_status else 1
    
    cursor.execute("UPDATE users SET is_active = ? WHERE id = ?", (new_status, user_id))
    conn.commit()
    conn.close()
    
    st.success(f"用户状态已更新")
    st.rerun()

def delete_user(user_id):
    """删除用户"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查是否试图删除自己
    if st.session_state.user['id'] == user_id:
        st.error("不能删除当前登录的用户")
        return
    
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    st.success("用户已删除")
    st.rerun()

def show_system_logs_page():
    """系统日志页面（供app.py调用）"""
    st.markdown("## 系统日志")
    
    # 这里可以集成实际的日志系统
    # 目前显示模拟数据
    logs = [
        {"time": "2026-05-29 10:30:00", "user": "admin", "action": "用户登录", "details": "管理员登录系统"},
        {"time": "2026-05-29 10:25:00", "user": "user1", "action": "数据上传", "details": "上传了销售数据.csv"},
        {"time": "2026-05-29 10:20:00", "user": "admin", "action": "用户管理", "details": "禁用用户 user2"},
    ]
    
    if not logs:
        st.info("暂无系统日志")
        return
    
    for log in logs:
        with st.expander(f"{log['time']} - {log['action']}"):
            st.write(f"**用户**: {log['user']}")
            st.write(f"**操作**: {log['action']}")
            st.write(f"**详情**: {log['details']}")

def show_system_management_page():
    """显示系统管理页面"""
    # 检查权限
    if not check_permission(st.session_state.user['role'], 'admin'):
        st.error("权限不足，需要管理员权限")
        return
    
    st.markdown("## 系统管理")
    
    # 创建标签页
    tab1, tab2 = st.tabs(["用户管理", "系统日志"])
    
    with tab1:
        show_user_management_page()
    
    with tab2:
        show_system_logs_page()
