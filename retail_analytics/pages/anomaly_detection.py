"""
Anomaly Detection Module - AI-powered anomaly detection and alerts
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import time

from data.database import execute_query
from config.settings import MIMO_CONFIG


def detect_anomalies(df, column, window=7, threshold=2):
    """
    使用统计方法检测异常
    参数：
        df: 包含日期和指定列的DataFrame
        column: 要检测异常的列名
        window: 滚动窗口大小（天）
        threshold: 标准差阈值
    返回：
        anomalies: 异常数据DataFrame
        df: 带异常评分的DataFrame
    """
    df = df.copy()
    df["rolling_mean"] = df[column].rolling(window=window, min_periods=1).mean()
    df["rolling_std"] = df[column].rolling(window=window, min_periods=1).std()
    
    # 计算Z-Score
    df["z_score"] = (df[column] - df["rolling_mean"]) / df["rolling_std"]
    
    # 标记异常（Z-Score绝对值超过阈值）
    df["is_anomaly"] = df["z_score"].abs() > threshold
    
    # 返回异常数据
    anomalies = df[df["is_anomaly"] == True].copy()
    
    return anomalies, df


def analyze_sales_anomalies():
    """Analyze sales anomalies"""
    # Query daily sales data
    query = """
    SELECT 
        DATE(order_date) as date,
        SUM(total_amount) as gmv,
        COUNT(DISTINCT order_id) as order_count,
        COUNT(DISTINCT user_id) as user_count
    FROM orders
    WHERE status != 'Cancelled'
    GROUP BY DATE(order_date)
    ORDER BY date DESC
    LIMIT 30
    """
    
    data = execute_query(query)
    
    if data.empty:
        return [], pd.DataFrame()
    
    data["date"] = pd.to_datetime(data["date"])
    
    # Detect GMV anomalies
    gmv_anomalies, gmv_df = detect_anomalies(data, "gmv", window=7, threshold=2)
    
    # Detect order count anomalies
    order_anomalies, order_df = detect_anomalies(data, "order_count", window=7, threshold=2)
    
    anomalies_list = []
    
    if not gmv_anomalies.empty:
        for _, row in gmv_anomalies.iterrows():
            anomalies_list.append({
                "date": row["date"].strftime("%Y-%m-%d"),
                "type": "GMV异常",
                "value": round(row["gmv"], 2),
                "expected": round(row["rolling_mean"], 2),
                "deviation": f"{row['z_score']:.2f}σ",
                "severity": "高" if abs(row["z_score"]) > 3 else "中"
            })
    
    if not order_anomalies.empty:
        for _, row in order_anomalies.iterrows():
            anomalies_list.append({
                "date": row["date"].strftime("%Y-%m-%d"),
                "type": "订单数异常",
                "value": int(row["order_count"]),
                "expected": round(row["rolling_mean"], 1),
                "deviation": f"{row['z_score']:.2f}σ",
                "severity": "高" if abs(row["z_score"]) > 3 else "中"
            })
    
    return anomalies_list, data


def analyze_user_anomalies():
    """Analyze user behavior anomalies"""
    # Query daily active users
    query = """
    SELECT 
        DATE(behavior_time) as date,
        COUNT(DISTINCT user_id) as active_users,
        COUNT(*) as behavior_count
    FROM user_behavior
    GROUP BY DATE(behavior_time)
    ORDER BY date DESC
    LIMIT 30
    """
    
    data = execute_query(query)
    
    if data.empty:
        return [], pd.DataFrame()
    
    data["date"] = pd.to_datetime(data["date"])
    
    # 检测活跃用户异常
    user_anomalies, user_df = detect_anomalies(data, "active_users", window=7, threshold=2)
    
    anomalies_list = []
    
    if not user_anomalies.empty:
        for _, row in user_anomalies.iterrows():
            anomalies_list.append({
                "date": row["date"].strftime("%Y-%m-%d"),
                "type": "活跃用户异常",
                "value": int(row["active_users"]),
                "expected": round(row["rolling_mean"], 1),
                "deviation": f"{row['z_score']:.2f}σ",
                "severity": "高" if abs(row["z_score"]) > 3 else "中"
            })
    
    return anomalies_list, data


def generate_ai_diagnosis(anomalies):
    """
    使用AI生成异常诊断报告
    """
    if not MIMO_CONFIG["api_key"] or not MIMO_CONFIG["base_url"]:
        # 模拟诊断（用于演示）
        return generate_mock_diagnosis(anomalies)
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=MIMO_CONFIG["api_key"],
            base_url=MIMO_CONFIG["base_url"]
        )
        
        # 构建提示词
        prompt = f"""
        请分析以下异常数据，并提供可能的原因和改进建议：
        
        异常数据：
        {anomalies}
        
        要求：
        1. 分析可能的原因（至少3个）
        2. 提供具体的改进建议（至少3个）
        3. 用中文回答，简洁专业
        """
        
        response = client.chat.completions.create(
            model=MIMO_CONFIG["model"],
            messages=[
                {"role": "system", "content": "你是一名专业的数据分析专家，擅长异常诊断。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ AI诊断失败：{str(e)}"


def generate_mock_diagnosis(anomalies):
    """生成模拟诊断报告（用于演示）"""
    if not anomalies:
        return "✅ 当前未检测到异常，系统运行正常。"
    
    diagnosis = """## 🔍 异常诊断报告

### 可能的原因

1. **外部因素**
   - 节假日或特殊事件导致用户行为变化
   - 竞争对手促销活动影响
   - 天气等不可抗力因素

2. **系统技术问题**
   - 服务器响应延迟导致用户流失
   - 支付系统故障
   - 数据库连接异常

3. **运营策略调整**
   - 促销活动结束，流量下降
   - 商品库存不足
   - 推荐算法调整导致转化率下降

### 改进建议

1. **短期措施（1-3天）**
   - 立即检查系统日志，排查技术故障
   - 联系客服收集用户反馈
   - 临时增加推广预算补充流量

2. **中期优化（1-2周）**
   - 优化页面加载速度
   - 调整推荐算法参数
   - 增加热门商品库存

3. **长期规划（1个月+）**
   - 建立完善的监控预警体系
   - 优化用户生命周期管理
   - 提升商品核心竞争力

---
**建议优先级**：先排查技术问题 → 再调整运营策略 → 最后优化产品体验
"""
    
    return diagnosis


def show_anomaly_detection_page():
    """异常检测页面"""
    st.markdown("## 🚨 异常检测播报")
    
    # 侧边栏设置
    with st.sidebar:
        st.markdown("### ⚙️ 检测设置")
        
        # 检测灵敏度
        threshold = st.slider(
            "检测灵敏度（标准差）",
            min_value=1.5,
            max_value=3.0,
            value=2.0,
            step=0.1,
            help="值越低越敏感（但误报率越高）"
        )
        
        # 检测窗口
        window = st.slider(
            "检测窗口（天）",
            min_value=3,
            max_value=14,
            value=7,
            help="用于计算基线的滚动窗口大小"
        )
        
        # 自动刷新
        auto_refresh = st.checkbox("自动刷新（30秒）", value=False)
        
        if auto_refresh:
            time.sleep(30)
            st.rerun()
    
    # Detect anomalies
    with st.spinner("正在检测异常..."):
        sales_anomalies, sales_data = analyze_sales_anomalies()
        user_anomalies, user_data = analyze_user_anomalies()
    
    all_anomalies = sales_anomalies + user_anomalies
    
    # 显示异常数量
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("检测到异常", len(all_anomalies))
    
    with col2:
        high_severity = len([a for a in all_anomalies if a["severity"] == "高"])
        st.metric("高风险异常", high_severity)
    
    with col3:
        if st.button("🔄 重新检测", use_container_width=True):
            st.rerun()
    
    # 异常列表
    if all_anomalies:
        st.markdown("### 🚨 异常列表")
        
        # 按严重程度排序
        all_anomalies_sorted = sorted(
            all_anomalies,
            key=lambda x: (x["severity"] == "高", x["date"]),
            reverse=True
        )
        
        # 显示异常表格
        df_anomalies = pd.DataFrame(all_anomalies_sorted)
        st.dataframe(df_anomalies, use_container_width=True)
        
        # 异常趋势图
        st.markdown("### 📊 异常趋势")
        
        # 合并销售数据用于可视化
        if not sales_data.empty:
            # 重新检测以绘图
            _, gmv_df = detect_anomalies(sales_data, "gmv", window=int(window), threshold=threshold)
            
            fig = px.line(
                gmv_df,
                x="date",
                y=["gmv", "rolling_mean"],
                title="GMV趋势与异常检测",
                labels={"value": "GMV (¥)", "date": "日期", "variable": "指标"},
                color_discrete_map={"gmv": "#1E88E5", "rolling_mean": "#FF6F00"}
            )
            
            # 标记异常点
            anomalies_df = gmv_df[gmv_df["is_anomaly"] == True]
            if not anomalies_df.empty:
                fig.add_scatter(
                    x=anomalies_df["date"],
                    y=anomalies_df["gmv"],
                    mode="markers",
                    marker=dict(size=12, color="red", symbol="x"),
                    name="异常点"
                )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # AI诊断
        st.markdown("### 🤖 AI智能诊断")
        
        if st.button("🔍 生成AI诊断报告", type="primary", use_container_width=True):
            with st.spinner("🤔 AI正在分析异常..."):
                diagnosis = generate_ai_diagnosis(all_anomalies)
                st.markdown(diagnosis)
        
        # 导出异常报告
        st.markdown("### 📥 导出异常报告")
        
        if st.button("📝 生成异常报告", use_container_width=True):
            report = generate_anomaly_report(all_anomalies)
            st.download_button(
                label="📥 下载异常报告 (CSV)",
                data=report,
                file_name=f"anomaly_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.success("✅ 当前未检测到异常，系统运行正常！")
        
        # Display normal trend chart
        if not sales_data.empty:
            fig = px.line(
                sales_data,
                x="date",
                y="gmv",
                title="GMV趋势 (正常)",
                labels={"gmv": "GMV (¥)", "date": "日期"}
            )
            fig.update_traces(line_color="#43A047")
            st.plotly_chart(fig, use_container_width=True)


def generate_anomaly_report(anomalies):
    """生成异常报告CSV"""
    if not anomalies:
        return "暂无异常数据"
    
    df = pd.DataFrame(anomalies)
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    
    return csv


if __name__ == "__main__":
    show_anomaly_detection_page()
