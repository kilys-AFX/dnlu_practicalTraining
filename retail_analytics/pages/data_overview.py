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
    """关键指标页面（柔和现代风）"""
    st.markdown("""
    <div class="page-header">
        <h1>核心指标总览</h1>
        <div class="breadcrumb">首页 / <span>数据概览</span> / 核心指标</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 检查数据
    users = execute_query("SELECT * FROM users LIMIT 1")
    orders = execute_query("SELECT * FROM orders LIMIT 1")
    
    if users.empty or orders.empty:
        st.warning("暂无数据，请先生成模拟数据")
        return
    
    # 计算指标
    total_users = execute_query("SELECT COUNT(DISTINCT user_id) as count FROM users").iloc[0]["count"]
    total_orders = execute_query("SELECT COUNT(DISTINCT order_id) as count FROM orders").iloc[0]["count"]
    total_gmv = execute_query("SELECT SUM(total_amount) as sum FROM orders WHERE status != 'Cancelled'").iloc[0]["sum"] or 0
    paid_users = execute_query("SELECT COUNT(DISTINCT user_id) as count FROM orders WHERE status != 'Cancelled'").iloc[0]["count"]
    conversion_rate = (paid_users / total_users * 100) if total_users > 0 else 0
    avg_order = total_gmv / total_orders if total_orders > 0 else 0
    
    # 指标卡片 - 柔和现代风
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""
        <div class="metric-card card-purple">
            <div class="metric-header">
                <div class="metric-icon-circle">👥</div>
                <div class="metric-badge">总用户</div>
            </div>
            <div class="metric-value">{total_users:,}</div>
            <div class="metric-label">注册用户总数</div>
            <div class="metric-change">↑ 12.5% vs 上月</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m2:
        st.markdown(f"""
        <div class="metric-card card-green">
            <div class="metric-header">
                <div class="metric-icon-circle">📦</div>
                <div class="metric-badge">订单</div>
            </div>
            <div class="metric-value">{total_orders:,}</div>
            <div class="metric-label">累计订单总数</div>
            <div class="metric-change">↑ 8.3% vs 上月</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m3:
        st.markdown(f"""
        <div class="metric-card card-blue">
            <div class="metric-header">
                <div class="metric-icon-circle">💰</div>
                <div class="metric-badge">GMV</div>
            </div>
            <div class="metric-value">¥{total_gmv:,.0f}</div>
            <div class="metric-label">累计销售额</div>
            <div class="metric-change">↑ 15.2% vs 上月</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m4:
        st.markdown(f"""
        <div class="metric-card card-orange">
            <div class="metric-header">
                <div class="metric-icon-circle">📈</div>
                <div class="metric-badge">转化</div>
            </div>
            <div class="metric-value">{conversion_rate:.1f}%</div>
            <div class="metric-label">整体转化率</div>
            <div class="metric-change">¥{avg_order:,.0f} 客单价</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 图表容器
    with st.container(border=True):
        st.markdown("### 📅 时间筛选与趋势分析")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            start_date = st.date_input("📅 开始日期", value=datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("📅 结束日期", value=datetime.now())
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            view_mode = st.selectbox("图表风格", ["面积图", "柱状图", "折线图"], label_visibility="collapsed")
        
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
            st.markdown("#### 📈 日活跃用户趋势")
            
            if view_mode == "面积图":
                fig1 = px.area(daily_data, x="date", y="active_users", 
                              labels={"active_users": "活跃用户数", "date": "日期"},
                              color_discrete_sequence=["#4F46E5"])
            elif view_mode == "柱状图":
                fig1 = px.bar(daily_data, x="date", y="active_users",
                             labels={"active_users": "活跃用户数", "date": "日期"},
                             color_discrete_sequence=["#4F46E5"])
            else:
                fig1 = px.line(daily_data, x="date", y="active_users", markers=True,
                              labels={"active_users": "活跃用户数", "date": "日期"},
                              color_discrete_sequence=["#4F46E5"])
            
            fig1.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0),
                              plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#E2E8F0'))
            st.plotly_chart(fig1, use_container_width=True)
            
            # 订单和GMV趋势
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                fig2 = px.line(daily_data, x="date", y="orders", markers=True,
                              labels={"orders": "订单数", "date": "日期"},
                              color_discrete_sequence=["#10B981"])
                fig2.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0),
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#E2E8F0'),
                                  title="日订单量趋势")
                st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                fig3 = px.bar(daily_data, x="date", y="gmv",
                             labels={"gmv": "GMV (¥)", "date": "日期"},
                             color_discrete_sequence=["#F59E0B"])
                fig3.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0),
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#E2E8F0'),
                                  title="日GMV趋势")
                st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("📭 选定时间范围内没有数据")


def show_trend_analysis_page():
    """趋势分析页面"""
    st.markdown("""
    <div class="page-header">
        <h1>趋势分析</h1>
        <div class="breadcrumb">首页 / <span>数据概览</span> / 趋势分析</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 用户增长趋势
    with st.container(border=True):
        st.markdown("### 📈 用户增长趋势")
        
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
            fig = px.area(user_growth, x="date", y="new_users",
                         labels={"new_users": "新增用户", "date": "日期"},
                         color_discrete_sequence=["#4F46E5"])
            fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0),
                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#E2E8F0'))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("暂无用户增长数据")
    
    # 留存趋势提示
    with st.container(border=True):
        st.markdown("### 🔄 用户留存趋势")
        st.info("💡 详细留存分析功能请前往「行为分析 → 留存分析」模块查看")


def show_user_portrait_page():
    """用户画像页面"""
    st.markdown("""
    <div class="page-header">
        <h1>用户画像分布</h1>
        <div class="breadcrumb">首页 / <span>数据概览</span> / 用户画像</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["性别分布", "年龄分布", "城市分布"])
    
    with tab1:
        gender_dist = execute_query("SELECT gender, COUNT(*) as count FROM users GROUP BY gender")
        
        if not gender_dist.empty:
            col1, col2 = st.columns([1, 1])
            with col1:
                fig1 = px.pie(gender_dist, values="count", names="gender",
                            color_discrete_sequence=["#4F46E5", "#EC4899", "#10B981"])
                fig1.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                st.dataframe(gender_dist, use_container_width=True, hide_index=True)
    
    with tab2:
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
            col1, col2 = st.columns([1, 1])
            with col1:
                fig2 = px.bar(age_dist, x="age_group", y="count",
                             labels={"count": "用户数", "age_group": "年龄段"},
                             color_discrete_sequence=["#06B6D4"])
                fig2.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0),
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)
            with col2:
                st.dataframe(age_dist, use_container_width=True, hide_index=True)
    
    with tab3:
        city_dist = execute_query("""
        SELECT city, COUNT(*) as count 
        FROM users 
        GROUP BY city 
        ORDER BY count DESC 
        LIMIT 10
        """)
        
        if not city_dist.empty:
            col1, col2 = st.columns([1, 1])
            with col1:
                fig3 = px.bar(city_dist, x="city", y="count",
                             labels={"count": "用户数", "city": "城市"},
                             color_discrete_sequence=["#F59E0B"])
                fig3.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0),
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig3, use_container_width=True)
            with col2:
                st.dataframe(city_dist, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    show_key_metrics_page()
