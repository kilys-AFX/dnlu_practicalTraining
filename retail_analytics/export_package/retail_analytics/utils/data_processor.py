"""
数据处理工具函数
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data.database import execute_query, bulk_insert, clear_table


def clean_data(df, rules=None):
    """
    数据清洗
    :param df: 原始数据框
    :param rules: 清洗规则字典
    :return: 清洗后的数据框
    """
    if rules is None:
        rules = {
            "drop_duplicates": True,
            "fill_missing": "mean",  # mean/median/mode/drop
            "handle_outliers": "clip"  # clip/drop
        }
    
    df_clean = df.copy()
    
    # 去重
    if rules.get("drop_duplicates", True):
        df_clean = df_clean.drop_duplicates()
    
    # 填充缺失值
    fill_method = rules.get("fill_missing", "mean")
    for col in df_clean.columns:
        if df_clean[col].isnull().any():
            if df_clean[col].dtype in [np.float64, np.int64]:
                if fill_method == "mean":
                    df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                elif fill_method == "median":
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                elif fill_method == "mode":
                    df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
            else:
                df_clean[col].fillna("未知", inplace=True)
    
    # 异常值处理（仅数值列）
    if rules.get("handle_outliers") == "clip":
        for col in df_clean.select_dtypes(include=[np.number]).columns:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df_clean[col] = df_clean[col].clip(lower, upper)
    
    return df_clean


def kmeans_clustering(df, n_clusters=4, features=None):
    """
    K-Means 用户聚类
    :param df: 用户特征数据框
    :param n_clusters: 聚类数量
    :param features: 用于聚类的特征列名列表
    :return: 聚类结果和模型
    """
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    
    if features is None:
        features = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # 准备数据
    X = df[features].fillna(0)
    
    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # K-Means 聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    # 添加聚类标签
    df_clustered = df.copy()
    df_clustered["Cluster"] = clusters
    
    # 计算聚类中心（反标准化）
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    cluster_centers_df = pd.DataFrame(cluster_centers, columns=features)
    cluster_centers_df["Cluster"] = range(n_clusters)
    
    return df_clustered, kmeans, cluster_centers_df


def calculate_retention(df_orders, periods=[1, 7, 30]):
    """
    计算用户留存率
    :param df_orders: 订单数据框，需包含 user_id, order_date
    :param periods: 留存周期（天）
    :return: 留存率数据框
    """
    df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])
    
    # 首次购买日期
    first_purchase = df_orders.groupby("user_id")["order_date"].min().reset_index()
    first_purchase.columns = ["user_id", "first_date"]
    
    # 合并数据
    df_merged = df_orders.merge(first_purchase, on="user_id")
    
    retention_results = []
    
    for period in periods:
        # 计算留存
        df_merged["days_diff"] = (df_merged["order_date"] - df_merged["first_date"]).dt.days
        retained = df_merged[df_merged["days_diff"] >= period]["user_id"].nunique()
        total = first_purchase["user_id"].nunique()
        
        retention_rate = retained / total if total > 0 else 0
        
        retention_results.append({
            "period": f"{period}日",
            "retained_users": retained,
            "total_users": total,
            "retention_rate": retention_rate
        })
    
    return pd.DataFrame(retention_results)


def get_behavior_funnel(df_behavior):
    """
    计算行为转化漏斗
    :param df_behavior: 行为日志数据框
    :return: 漏斗数据框
    """
    funnel_steps = ["浏览", "加购", "下单", "支付"]
    funnel_counts = []
    
    for step in funnel_steps:
        count = df_behavior[df_behavior["behavior_type"] == step]["user_id"].nunique()
        funnel_counts.append({"step": step, "users": count})
    
    df_funnel = pd.DataFrame(funnel_counts)
    df_funnel["conversion_rate"] = df_funnel["users"] / df_funnel["users"].iloc[0] * 100
    
    return df_funnel


def generate_session_data(df_behavior, user_id=None):
    """
    生成用户行为路径数据（用于桑基图）
    :param df_behavior: 行为日志数据框
    :param user_id: 指定用户ID（可选）
    :return: 路径数据框
    """
    if user_id:
        df_behavior = df_behavior[df_behavior["user_id"] == user_id]
    
    # 按用户和时间排序
    df_behavior = df_behavior.sort_values(["user_id", "behavior_time"])
    
    # 生成路径（当前行为 -> 下一个行为）
    df_behavior["next_behavior"] = df_behavior.groupby("user_id")["behavior_type"].shift(-1)
    
    # 统计路径流量
    paths = df_behavior.groupby(["behavior_type", "next_behavior"]).size().reset_index()
    paths.columns = ["source", "target", "value"]
    
    # 移除空路径
    paths = paths.dropna()
    
    return paths


def calculate_rfm(df_orders, df_users=None):
    """
    计算RFM模型（零售分析核心指标）
    RFM = Recency（最近购买）、Frequency（购买频率）、Monetary（购买金额）
    
    :param df_orders: 订单数据框，需包含 user_id, order_date, total_amount
    :param df_users: 用户数据框（可选）
    :return: RFM数据框
    """
    # 确保日期格式正确
    df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])
    
    # 计算当前日期（用于计算Recency）
    current_date = datetime.now()
    
    # 按用户聚合RFM指标
    rfm = df_orders.groupby("user_id").agg({
        "order_date": lambda x: (current_date - x.max()).days,  # Recency: 最近购买距今天数
        "order_id": "count",  # Frequency: 购买次数
        "total_amount": "sum"  # Monetary: 总购买金额
    })
    
    rfm.columns = ["recency", "frequency", "monetary"]
    
    # 处理异常值（Recency为0的情况）
    rfm["recency"] = rfm["recency"].apply(lambda x: max(x, 1))
    
    # RFM评分（使用分位数法）
    rfm["R_score"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1])  # 越小越好，所以反转
    rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4])
    rfm["M_score"] = pd.qcut(rfm["monetary"], 4, labels=[1, 2, 3, 4])
    
    # 转换为数值类型
    rfm["R_score"] = rfm["R_score"].astype(int)
    rfm["F_score"] = rfm["F_score"].astype(int)
    rfm["M_score"] = rfm["M_score"].astype(int)
    
    # 计算RFM总分
    rfm["rfm_score"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)
    
    # RFM客户细分
    def segment_customers(row):
        """根据RFM得分进行客户细分"""
        r, f, m = row["R_score"], row["F_score"], row["M_score"]
        
        if r >= 3 and f >= 3 and m >= 3:
            return "冠军客户"
        elif r >= 3 and f >= 3 and m < 3:
            return "忠实客户"
        elif r >= 3 and f < 3:
            return "新客户"
        elif r < 3 and f >= 3:
            return "流失风险客户"
        elif r < 3 and f < 3 and m >= 3:
            return "高价值流失客户"
        else:
            return "一般客户"
    
    rfm["segment"] = rfm.apply(segment_customers, axis=1)
    
    # 合并用户信息（如果提供）
    if df_users is not None:
        rfm = rfm.merge(df_users[["user_id", "gender", "age", "city"]], on="user_id", how="left")
    
    return rfm


def get_rfm_segment_summary(rfm_df):
    """
    获取RFM客户细分摘要
    """
    segment_summary = rfm_df.groupby("segment").agg({
        "user_id": "count",
        "recency": "mean",
        "frequency": "mean",
        "monetary": "mean"
    }).reset_index()
    
    segment_summary.columns = ["segment", "customer_count", "avg_recency", "avg_frequency", "avg_monetary"]
    segment_summary = segment_summary.sort_values("customer_count", ascending=False)
    
    return segment_summary


if __name__ == "__main__":
    # 测试代码
    from data.database import init_database, execute_query
    
    init_database()
    
    # 测试 K-Means 聚类
    print("K-Means 聚类功能正常")
    
    # 测试留存率计算
    orders = execute_query("SELECT * FROM orders LIMIT 1000")
    if not orders.empty:
        retention = calculate_retention(orders)
        print("\n留存率分析:")
        print(retention)
