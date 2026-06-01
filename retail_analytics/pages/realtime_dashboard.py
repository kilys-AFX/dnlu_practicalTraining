"""
实时数据大屏 - 模拟实时数据显示
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
from streamlit_autorefresh import st_autorefresh

from data.database import execute_query


def show_realtime_dashboard():
    """实时数据大屏页面"""
    st.markdown("## 📊 实时数据大屏")
    
    # 自动刷新（每5秒刷新一次）
    st_autorefresh(interval=5000, key="realtime_refresh")
    
    # 侧边栏设置
    with st.sidebar:
        st.markdown("### ⚙️ 大屏设置")
        
        # 刷新频率
        refresh_interval = st.selectbox(
            "刷新频率（秒）",
            [5, 10, 30, 60],
            index=0
        )
        
        # 模拟数据开关
        simulate_data = st.checkbox("模拟实时数据", value=True)
        
        if st.button("立即刷新", use_container_width=True):
            st.rerun()
    
    # 获取实时数据
    if simulate_data:
        realtime_data = generate_mock_realtime_data()
    else:
        realtime_data = get_realtime_data()
    
    # 仪表盘布局
    # 第一行：关键指标卡片
    st.markdown("### 📊 实时关键指标")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="在线用户",
            value=f"{realtime_data['online_users']}",
            delta=random.randint(-50, 100)
        )
    
    with col2:
        st.metric(
            label="今日订单",
            value=f"{realtime_data['today_orders']}",
            delta=random.randint(10, 200)
        )
    
    with col3:
        st.metric(
            label="今日GMV",
            value=f"¥{realtime_data['today_gmv']:.2f}",
            delta=round(random.uniform(-5000, 20000), 2)
        )
    
    with col4:
        st.metric(
            label="转化率",
            value=f"{realtime_data['conversion_rate']:.2f}%",
            delta=round(random.uniform(-0.5, 2.0), 2)
        )
    
    # 第二行：实时趋势图
    st.markdown("### 📈 实时订单趋势")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 今日每小时订单趋势
        fig1 = px.line(
            realtime_data['hourly_orders'],
            x="hour",
            y="orders",
            title="今日每小时订单量",
            labels={"hour": "小时", "orders": "订单量"}
        )
        fig1.update_traces(line_color="#1E88E5")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 今日GMV趋势
        fig2 = px.area(
            realtime_data['hourly_gmv'],
            x="hour",
            y="gmv",
            title="今日GMV趋势",
            labels={"hour": "小时", "gmv": "GMV (¥)"}
        )
        fig2.update_traces(line_color="#FF6F00", fillcolor="rgba(255,111,0,0.2)")
        st.plotly_chart(fig2, use_container_width=True)
    
    # 第三行：实时排行榜
    st.markdown("### 🏆 热销商品TOP 10")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 热销商品排行
        fig3 = px.bar(
            realtime_data['top_products'],
            x="sales",
            y="product_name",
            orientation='h',
            title="热销商品排行",
            labels={"sales": "销量", "product_name": "商品名称"},
            color="sales",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # 品类销售占比
        fig4 = px.pie(
            realtime_data['category_sales'],
            values="sales",
            names="category",
            title="品类销售占比"
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # 第四行：实时订单流
    st.markdown("### 📋 实时订单流")
    
    # 显示最近20条订单
    order_feed = realtime_data['recent_orders']
    
    for idx, order in enumerate(order_feed.itertuples()):
        col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
        
        with col1:
            st.caption(f"#{order.order_id}")
        
        with col2:
            st.caption(f"用户 {order.user_id}")
        
        with col3:
            st.caption(f"¥{order.total_amount:.2f}")
        
        with col4:
            status_color = {
                "Pending": "🟡",
                "Paid": "🔵",
                "Shipped": "🟢",
                "Completed": "✅",
                "Cancelled": "🔴"
            }.get(order.status, "⚪")
            
            # 状态中文映射
            status_text = {
                "Pending": "待处理",
                "Paid": "已支付",
                "Shipped": "已发货",
                "Completed": "已完成",
                "Cancelled": "已取消"
            }.get(order.status, order.status)
            
            st.caption(f"{status_color} {status_text}")
        
        if idx < len(order_feed) - 1:
            st.divider()
    
    # 第五行：系统状态
    st.markdown("### ⚙️ 系统状态")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"数据采集延迟：{random.randint(10, 100)} ms")
    
    with col2:
        st.info(f"数据处理速率：{random.randint(1000, 5000)} 条/秒")
    
    with col3:
        st.info(f"最后更新：{datetime.now().strftime('%H:%M:%S')}")


def generate_mock_realtime_data():
    """生成模拟实时数据"""
    # 实时关键指标
    online_users = random.randint(800, 2000)
    today_orders = random.randint(500, 1500)
    today_gmv = random.uniform(50000, 200000)
    conversion_rate = random.uniform(3.5, 8.5)
    
    # 今日每小时订单趋势
    hourly_orders = pd.DataFrame({
        "hour": [f"{i}:00" for i in range(24)],
        "orders": [random.randint(10, 100) for _ in range(24)]
    })
    
    # 今日每小时 GMV 趋势
    hourly_gmv = pd.DataFrame({
        "hour": [f"{i}:00" for i in range(24)],
        "gmv": [random.uniform(1000, 10000) for _ in range(24)]
    })
    
    # 热销商品 TOP 10
    top_products = pd.DataFrame({
        "product_name": [f"商品{i}" for i in range(1, 11)],
        "sales": [random.randint(50, 500) for _ in range(10)]
    })
    
    # 品类销售占比
    category_sales = pd.DataFrame({
        "category": ["服装", "电子产品", "食品", "家居", "美妆"],
        "sales": [random.randint(100, 1000) for _ in range(5)]
    })
    
    # 最近订单流
    recent_orders = pd.DataFrame({
        "order_id": [random.randint(10000, 99999) for _ in range(20)],
        "user_id": [random.randint(1, 1000) for _ in range(20)],
        "total_amount": [random.uniform(50, 2000) for _ in range(20)],
        "status": random.choices(
            ["Pending", "Paid", "Shipped", "Completed", "Cancelled"],
            weights=[10, 15, 20, 45, 10],
            k=20
        )
    })
    
    return {
        "online_users": online_users,
        "today_orders": today_orders,
        "today_gmv": today_gmv,
        "conversion_rate": conversion_rate,
        "hourly_orders": hourly_orders,
        "hourly_gmv": hourly_gmv,
        "top_products": top_products,
        "category_sales": category_sales,
        "recent_orders": recent_orders
    }


def get_realtime_data():
    """Get real-time data from database"""
    # Get today's data
    today = datetime.now().date()
    
    # Today's order count
    today_orders = execute_query("""
    SELECT COUNT(*) as count
    FROM orders
    WHERE DATE(order_date) = ?
    """, (today,)).iloc[0]["count"]
    
    # Today's GMV
    today_gmv = execute_query("""
    SELECT SUM(total_amount) as sum
    FROM orders
    WHERE DATE(order_date) = ? AND status != 'Cancelled'
    """, (today,)).iloc[0]["sum"] or 0
    
    # Online users (simulated)
    online_users = random.randint(800, 2000)
    
    # Conversion rate (simulated)
    conversion_rate = random.uniform(3.5, 8.5)
    
    # Today's hourly order trend (simulated)
    hourly_orders = pd.DataFrame({
        "hour": [f"{i}:00" for i in range(24)],
        "orders": [random.randint(10, 100) for _ in range(24)]
    })
    
    # Today's hourly GMV trend (simulated)
    hourly_gmv = pd.DataFrame({
        "hour": [f"{i}:00" for i in range(24)],
        "gmv": [random.uniform(1000, 10000) for _ in range(24)]
    })
    
    # Top 10 best-selling products (query from database)
    top_products = execute_query("""
    SELECT p.product_name, SUM(oi.quantity) as sales
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE DATE(o.order_date) = ? AND o.status != 'Cancelled'
    GROUP BY p.product_id
    ORDER BY sales DESC
    LIMIT 10
    """, (today,))
    
    if top_products.empty:
        top_products = pd.DataFrame({
            "product_name": [f"Product {i}" for i in range(1, 11)],
            "sales": [random.randint(50, 500) for _ in range(10)]
        })
    
    # Sales by category
    category_sales = execute_query("""
    SELECT p.category, SUM(oi.quantity) as sales
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE DATE(o.order_date) = ? AND o.status != 'Cancelled'
    GROUP BY p.category
    """, (today,))
    
    if category_sales.empty:
        category_sales = pd.DataFrame({
            "category": ["Clothing", "Electronics", "Food", "Home", "Beauty"],
            "sales": [random.randint(100, 1000) for _ in range(5)]
        })
    
    # Recent order feed
    recent_orders = execute_query("""
    SELECT order_id, user_id, total_amount, status
    FROM orders
    ORDER BY order_date DESC
    LIMIT 20
    """)
    
    if recent_orders.empty:
        recent_orders = pd.DataFrame({
            "order_id": [random.randint(10000, 99999) for _ in range(20)],
            "user_id": [random.randint(1, 1000) for _ in range(20)],
            "total_amount": [random.uniform(50, 2000) for _ in range(20)],
            "status": random.choices(
                ["Pending", "Paid", "Shipped", "Completed", "Cancelled"],
                weights=[10, 15, 20, 45, 10],
                k=20
            )
        })
    
    return {
        "online_users": online_users,
        "today_orders": today_orders,
        "today_gmv": today_gmv,
        "conversion_rate": conversion_rate,
        "hourly_orders": hourly_orders,
        "hourly_gmv": hourly_gmv,
        "top_products": top_products,
        "category_sales": category_sales,
        "recent_orders": recent_orders
    }


if __name__ == "__main__":
    show_realtime_dashboard()
