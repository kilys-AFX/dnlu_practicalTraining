"""
用户画像模块 - 用户聚类/生命周期
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from data.database import execute_query
from utils.data_processor import kmeans_clustering


def show_clustering_page():
    """用户聚类页面"""
    st.markdown("## 🎯 K-Means 用户聚类")
    
    # 查询用户特征数据
    query = """
    SELECT 
        u.user_id,
        u.age,
        u.gender,
        COUNT(DISTINCT o.order_id) as order_count,
        SUM(o.total_amount) as total_spent,
        AVG(o.total_amount) as avg_order_value,
        MAX(o.order_date) as last_order_date,
        julianday('now') - julianday(MAX(o.order_date)) as days_since_last_order
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id
    WHERE o.status != 'Cancelled' OR o.status IS NULL
    GROUP BY u.user_id
    """
    
    users = execute_query(query)
    
    if users.empty:
        st.warning("⚠️ 暂无用户数据")
        return
    
    # 特征选择
    st.markdown("### ⚙️ 聚类设置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_clusters = st.slider("聚类数量", min_value=2, max_value=10, value=4)
    
    with col2:
        features = st.multiselect(
            "选择特征",
            options=["age", "order_count", "total_spent", "avg_order_value", "days_since_last_order"],
            default=["order_count", "total_spent", "days_since_last_order"]
        )
    
    if not features:
        st.warning("⚠️ 请至少选择一个特征")
        return
    
    # 执行聚类
    if st.button("🚀 执行聚类", type="primary"):
        with st.spinner("正在进行K-Means聚类..."):
            # 准备数据
            df_features = users[["user_id"] + features].fillna(0)
            
            # 聚类
            df_clustered, kmeans_model, cluster_centers = kmeans_clustering(
                df_features,
                n_clusters=n_clusters,
                features=features
            )
            
            # 保存结果到session_state
            st.session_state["clustering_result"] = df_clustered
            st.session_state["cluster_centers"] = cluster_centers
            
            st.success("✅ 聚类完成！")
    
    # 显示聚类结果
    if "clustering_result" in st.session_state:
        df_clustered = st.session_state["clustering_result"]
        cluster_centers = st.session_state["cluster_centers"]
        
        # 聚类分布
        st.markdown("### 📊 聚类分布")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cluster_counts = df_clustered["Cluster"].value_counts().sort_index().reset_index()
            cluster_counts.columns = ["Cluster", "Count"]
            
            fig1 = px.bar(
                cluster_counts,
                x="Cluster",
                y="Count",
                title="各聚类用户数量",
                labels={"Cluster": "聚类编号", "Count": "用户数"}
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # 聚类中心雷达图
            fig2 = go.Figure()
            
            for i in range(n_clusters):
                cluster_data = cluster_centers.iloc[i]
                values = cluster_data[features].tolist()
                values.append(values[0])  # 闭合雷达图
                
                fig2.add_trace(go.Scatterpolar(
                    r=values,
                    theta=features + [features[0]],
                    fill='toself',
                    name=f'聚类 {i}'
                ))
            
            fig2.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True
                    )),
                showlegend=True,
                title="聚类中心特征对比"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # 聚类详情表格
        st.markdown("### 📋 聚类详情")
        st.dataframe(df_clustered, use_container_width=True)
        
        # 下载结果
        if st.button("📥 下载聚类结果"):
            csv = df_clustered.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="下载CSV",
                data=csv,
                file_name="user_clustering.csv",
                mime="text/csv"
            )


def show_lifecycle_page():
    """用户生命周期页面"""
    st.markdown("## 🔄 用户生命周期管理")
    
    # 查询用户生命周期数据
    query = """
    SELECT 
        u.user_id,
        u.register_date,
        u.last_login,
        COUNT(DISTINCT o.order_id) as order_count,
        MAX(o.order_date) as last_order_date,
        julianday('now') - julianday(u.register_date) as days_since_register,
        CASE 
            WHEN julianday('now') - julianday(MAX(o.order_date)) IS NULL THEN NULL
            ELSE julianday('now') - julianday(MAX(o.order_date))
        END as days_since_last_order
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id
    GROUP BY u.user_id
    """
    
    users = execute_query(query)
    
    if users.empty:
        st.warning("⚠️ 暂无用户数据")
        return
    
    # 计算生命周期阶段
    def classify_lifecycle(row):
        if row["order_count"] == 0:
            return "潜在客户"
        elif row["days_since_last_order"] is None or row["days_since_last_order"] > 90:
            return "流失客户"
        elif row["days_since_last_order"] > 30:
            return "流失预警"
        elif row["order_count"] <= 3:
            return "新客户"
        else:
            return "忠实客户"
    
    users["lifecycle"] = users.apply(classify_lifecycle, axis=1)
    
    # 生命周期分布
    st.markdown("### 📊 生命周期分布")
    
    lifecycle_counts = users["lifecycle"].value_counts().reset_index()
    lifecycle_counts.columns = ["Lifecycle", "Count"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.pie(
            lifecycle_counts,
            values="Count",
            names="Lifecycle",
            title="用户生命周期分布"
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(
            lifecycle_counts,
            x="Lifecycle",
            y="Count",
            title="各生命周期用户数量",
            labels={"Lifecycle": "生命周期阶段", "Count": "用户数"}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # 生命周期详情
    st.markdown("### 📋 生命周期详情")
    
    selected_lifecycle = st.selectbox(
        "筛选生命周期阶段",
        options=["全部"] + list(users["lifecycle"].unique())
    )
    
    if selected_lifecycle == "全部":
        filtered_users = users
    else:
        filtered_users = users[users["lifecycle"] == selected_lifecycle]
    
    st.dataframe(filtered_users, use_container_width=True)
    
    # 运营建议
    st.markdown("### 💡 运营建议")
    
    lost_users = len(users[users["lifecycle"] == "流失客户"])
    warning_users = len(users[users["lifecycle"] == "流失预警"])
    
    if lost_users > 0:
        st.warning(f"⚠️ 发现 {lost_users} 名流失客户，建议发送召回优惠券")
    
    if warning_users > 0:
        st.info(f"ℹ️ 发现 {warning_users} 名流失预警客户，建议及时跟进")


if __name__ == "__main__":
    show_rfm_page()
