"""
数据概览模块 - 关键指标/趋势分析/用户画像
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from data.database import execute_query


def show_key_metrics_page():
    """关键指标页面"""
    st.markdown("## 📊 关键指标")
    
    # 检查数据是否存在
    users = execute_query("SELECT * FROM users LIMIT 1")
    orders = execute_query("SELECT * FROM orders LIMIT 1")
    
    if users.empty or orders.empty:
        st.warning("⚠️ 暂无数据，请先上传数据或生成模拟数据")
        return
    
    # 计算关键指标
    total_users = execute_query("SELECT COUNT(DISTINCT user_id) as count FROM users").iloc[0]["count"]
    total_orders = execute_query("SELECT COUNT(DISTINCT order_id) as count FROM orders").iloc[0]["count"]
    total_gmv = execute_query("SELECT SUM(total_amount) as sum FROM orders WHERE status != 'Cancelled'").iloc[0]["sum"]
    total_gmv = total_gmv if total_gmv else 0
    
    # 转化率（有支付的用户/总用户）
    paid_users = execute_query("SELECT COUNT(DISTINCT user_id) as count FROM orders WHERE status != 'Cancelled'").iloc[0]["count"]
    conversion_rate = (paid_users / total_users * 100) if total_users > 0 else 0
    
    # 显示指标卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="总用户数",
            value=f"{total_users:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="总订单数",
            value=f"{total_orders:,}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="GMV（销售额）",
            value=f"¥{total_gmv:,.2f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="转化率",
            value=f"{conversion_rate:.2f}%",
            delta=None
        )
    
    # 时间筛选器
    st.markdown("### 📅 时间筛选")
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "开始日期",
            value=datetime.now() - timedelta(days=30)
        )
    
    with col2:
        end_date = st.date_input(
            "结束日期",
            value=datetime.now()
        )
    
    # 趋势图
    st.markdown("### 📈 日活跃趋势")
    
    # 查询每日订单数
    query = """
    SELECT 
        DATE(order_date) as date,
        COUNT(DISTINCT user_id) as active_users,
        COUNT(DISTINCT order_id) as orders,
        SUM(total_amount) as gmv
    FROM orders
    WHERE DATE(order_date) BETWEEN ? AND ?
    GROUP BY DATE(order_date)
    ORDER BY date
    """
    
    daily_data = execute_query(query, (start_date, end_date))
    
    if not daily_data.empty:
        # 活跃用户趋势
        fig1 = px.area(
            daily_data,
            x="date",
            y="active_users",
            title="日活跃用户趋势",
            labels={"active_users": "活跃用户数", "date": "日期"}
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # 订单和GMV趋势
        col1, col2 = st.columns(2)
        
        with col1:
            fig2 = px.line(
                daily_data,
                x="date",
                y="orders",
                title="日订单量趋势",
                labels={"orders": "订单数", "date": "日期"}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            fig3 = px.bar(
                daily_data,
                x="date",
                y="gmv",
                title="日GMV趋势",
                labels={"gmv": "GMV (¥)", "date": "日期"}
            )
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("📭 选定时间范围内没有数据")


def show_trend_analysis_page():
    """趋势分析页面"""
    st.markdown("## 📈 趋势分析")
    
    # 用户增长趋势
    st.markdown("### 用户增长趋势")
    
    query = """
    SELECT 
        DATE(register_date) as date,
        COUNT(*) as new_users
    FROM users
    GROUP BY DATE(register_date)
    ORDER BY date
    """
    
    user_growth = execute_query(query)
    
    if not user_growth.empty:
        fig = px.line(
            user_growth,
            x="date",
            y="new_users",
            title="每日新增用户趋势",
            labels={"new_users": "新增用户", "date": "日期"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 留存趋势（简化版）
    st.markdown("### 用户留存趋势")
    st.info("💡 留存分析功能在「行为分析 - 留存分析」模块中")


def show_user_portrait_page():
    """用户画像页面"""
    st.markdown("## 👤 用户画像分布")
    
    # 性别分布
    st.markdown("### 性别分布")
    gender_dist = execute_query("SELECT gender, COUNT(*) as count FROM users GROUP BY gender")
    
    if not gender_dist.empty:
        fig1 = px.pie(
            gender_dist,
            values="count",
            names="gender",
            title="用户性别分布"
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    # 年龄分布
    st.markdown("### 年龄分布")
    age_dist = execute_query("""
    SELECT 
        CASE 
            WHEN age < 20 THEN '20岁以下'
            WHEN age BETWEEN 20 AND 30 THEN '20-30岁'
            WHEN age BETWEEN 31 AND 40 THEN '31-40岁'
            WHEN age BETWEEN 41 AND 50 THEN '41-50岁'
            ELSE '50岁以上'
        END as age_group,
        COUNT(*) as count
    FROM users
    GROUP BY age_group
    ORDER BY age_group
    """)
    
    if not age_dist.empty:
        fig2 = px.bar(
            age_dist,
            x="age_group",
            y="count",
            title="用户年龄分布",
            labels={"count": "用户数", "age_group": "年龄段"}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # 城市分布
    st.markdown("### 城市分布")
    city_dist = execute_query("""
    SELECT city, COUNT(*) as count 
    FROM users 
    GROUP BY city 
    ORDER BY count DESC 
    LIMIT 10
    """)
    
    if not city_dist.empty:
        fig3 = px.bar(
            city_dist,
            x="city",
            y="count",
            title="用户城市分布 TOP 10",
            labels={"count": "用户数", "city": "城市"}
        )
        st.plotly_chart(fig3, use_container_width=True)


if __name__ == "__main__":
    show_key_metrics_page()
