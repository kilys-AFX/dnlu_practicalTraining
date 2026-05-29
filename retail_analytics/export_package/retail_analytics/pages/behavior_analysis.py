"""
行为分析模块 - 热力图/漏斗图/留存曲线/行为路径
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from data.database import execute_query
from utils.data_processor import calculate_retention, get_behavior_funnel, generate_session_data


def show_heatmap_page():
    """用户活跃热力图页面"""
    st.markdown("## 🔥 用户活跃热力图")
    
    # 查询行为数据
    query = """
    SELECT 
        strftime('%w', behavior_time) as weekday,
        strftime('%H', behavior_time) as hour,
        COUNT(DISTINCT user_id) as active_users
    FROM user_behavior
    GROUP BY weekday, hour
    ORDER BY weekday, hour
    """
    
    data = execute_query(query)
    
    if data.empty:
        st.warning("⚠️ 暂无行为数据，请先上传数据或生成模拟数据")
        return
    
    # 转换星期几为文字
    weekday_map = {"0": "周日", "1": "周一", "2": "周二", "3": "周三", "4": "周四", "5": "周五", "6": "周六"}
    data["weekday_name"] = data["weekday"].astype(str).map(weekday_map)
    
    # 创建热力图数据
    heatmap_data = data.pivot(index="weekday_name", columns="hour", values="active_users").fillna(0)
    
    # 重新排序星期
    weekday_order = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    heatmap_data = heatmap_data.reindex(weekday_order)
    
    # 绘制热力图
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="小时", y="星期", color="活跃用户数"),
        x=[f"{i}:00" for i in range(24)],
        y=weekday_order,
        title="用户活跃热力图（按小时×星期）",
        color_continuous_scale="Blues"
    )
    
    fig.update_layout(
        xaxis_title="小时",
        yaxis_title="星期",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 洞察
    st.markdown("### 💡 数据洞察")
    peak_hour = data.loc[data["active_users"].idxmax()]
    st.info(f"📊 用户最活跃时段：{peak_hour['hour']}:00-{int(peak_hour['hour'])+1}:00，活跃用户数 {int(peak_hour['active_users'])}")


def show_funnel_page():
    """购买转化漏斗页面"""
    st.markdown("## 🏀 购买转化漏斗")
    
    # 计算漏斗数据
    query = """
    SELECT behavior_type, COUNT(DISTINCT user_id) as users
    FROM user_behavior
    WHERE behavior_type IN ('浏览', '加购', '下单', '支付')
    GROUP BY behavior_type
    ORDER BY 
        CASE behavior_type
            WHEN '浏览' THEN 1
            WHEN '加购' THEN 2
            WHEN '下单' THEN 3
            WHEN '支付' THEN 4
        END
    """
    
    funnel_data = execute_query(query)
    
    if funnel_data.empty:
        st.warning("⚠️ 暂无行为数据")
        return
    
    # 计算转化率
    funnel_data["conversion_rate"] = funnel_data["users"] / funnel_data["users"].iloc[0] * 100
    
    # 绘制漏斗图
    fig = go.Figure(go.Funnel(
        y=funnel_data["behavior_type"],
        x=funnel_data["users"],
        textinfo="value+percent initial",
        marker_color=["#1E88E5", "#5E35B1", "#FF6F00", "#43A047"]
    ))
    
    fig.update_layout(
        title="用户购买转化漏斗",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示数据表格
    st.markdown("### 📊 转化数据详情")
    st.dataframe(funnel_data, use_container_width=True)
    
    # 洞察
    st.markdown("### 💡 优化建议")
    if len(funnel_data) >= 4:
        browse_to_cart = funnel_data.iloc[1]["users"] / funnel_data.iloc[0]["users"] * 100
        cart_to_order = funnel_data.iloc[2]["users"] / funnel_data.iloc[1]["users"] * 100
        order_to_pay = funnel_data.iloc[3]["users"] / funnel_data.iloc[2]["users"] * 100
        
        if browse_to_cart < 20:
            st.warning(f"⚠️ 浏览到加购转化率仅 {browse_to_cart:.1f}%，建议优化商品详情页")
        if cart_to_order < 50:
            st.warning(f"⚠️ 加购到下单转化率仅 {cart_to_order:.1f}%，建议优化购物车体验")
        if order_to_pay < 80:
            st.warning(f"⚠️ 下单到支付转化率仅 {order_to_pay:.1f}%，建议简化支付流程")


def show_retention_page():
    """用户留存曲线页面"""
    st.markdown("## 🔄 用户留存分析")
    
    # 查询订单数据
    query = """
    SELECT 
        user_id,
        DATE(order_date) as order_date
    FROM orders
    WHERE status != 'Cancelled'
    ORDER BY user_id, order_date
    """
    
    orders = execute_query(query)
    
    if orders.empty:
        st.warning("⚠️ 暂无订单数据")
        return
    
    # 计算留存
    retention_data = calculate_retention(orders, periods=[1, 3, 7, 14, 30])
    
    # 绘制留存曲线
    fig = px.line(
        retention_data,
        x="period",
        y="retention_rate",
        title="用户留存曲线",
        labels={"retention_rate": "留存率 (%)", "period": "天数"},
        markers=True
    )
    
    fig.update_layout(
        yaxis_tickformat=".1%",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示数据表格
    st.markdown("### 📊 留存数据详情")
    retention_data["retention_rate"] = retention_data["retention_rate"].apply(lambda x: f"{x:.2%}")
    st.dataframe(retention_data, use_container_width=True)


def show_behavior_path_page():
    """用户行为路径页面（桑基图）"""
    st.markdown("## 🕸️ 用户行为路径分析")
    
    # 查询行为数据
    query = """
    SELECT 
        user_id,
        behavior_type,
        behavior_time
    FROM user_behavior
    ORDER BY user_id, behavior_time
    LIMIT 10000
    """
    
    behavior = execute_query(query)
    
    if behavior.empty:
        st.warning("⚠️ 暂无行为数据")
        return
    
    # 生成路径数据
    paths = generate_session_data(behavior)
    
    if paths.empty:
        st.warning("⚠️ 无法生成行为路径")
        return
    
    # 创建桑基图
    # 收集所有节点
    all_nodes = pd.concat([paths["source"], paths["target"]]).unique().tolist()
    node_indices = {node: i for i, node in enumerate(all_nodes)}
    
    # 构建桑基图数据
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color="blue"
        ),
        link=dict(
            source=[node_indices[src] for src in paths["source"]],
            target=[node_indices[tgt] for tgt in paths["target"]],
            value=paths["value"]
        )
    ))
    
    fig.update_layout(
        title="用户行为路径桑基图",
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 💡 说明")
    st.info("桑基图的宽度代表用户流量，可以直观看到用户在各行为之间的流转情况")


if __name__ == "__main__":
    show_heatmap_page()
