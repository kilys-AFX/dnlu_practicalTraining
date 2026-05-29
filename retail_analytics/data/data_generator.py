"""
模拟数据生成器 - 生成零售业务测试数据
"""
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from config.settings import DATABASE_PATH, MODEL_CONFIG

# 设置随机种子
np.random.seed(MODEL_CONFIG["random_state"])
random.seed(MODEL_CONFIG["random_state"])

# 常量定义
CITIES = ["北京", "上海", "广州", "杭州", "深圳", "成都", "武汉", "南京", "西安", "重庆"]
CATEGORIES = ["服装", "电子产品", "食品", "家居", "美妆", "图书", "运动", "母婴"]
BEHAVIOR_TYPES = ["浏览", "加购", "收藏", "下单", "支付"]
DEVICES = ["iOS", "Android", "PC", "微信小程序"]
CHANNELS = ["搜索", "推荐", "广告", "社交媒体", "直接访问"]
ORDER_STATUSES = ["待付款", "已付款", "已发货", "已完成", "已取消"]


def generate_users(num_users=1000):
    """生成用户数据"""
    users = []
    for user_id in range(1, num_users + 1):
        gender = random.choice(["男", "女"])
        age = int(np.random.normal(35, 10))  # 正态分布，均值35，标准差10
        age = max(18, min(70, age))  # 限制在18-70岁
        city = random.choice(CITIES)
        
        # 注册日期：过去2年内随机
        days_ago = random.randint(1, 730)
        register_date = (datetime.now() - timedelta(days=days_ago)).date()
        
        # 最后登录：最近30天内随机
        last_login_days = random.randint(0, 30)
        last_login = (datetime.now() - timedelta(days=last_login_days)).date()
        
        users.append({
            "user_id": user_id,
            "gender": gender,
            "age": age,
            "city": city,
            "register_date": register_date.isoformat(),
            "last_login": last_login.isoformat()
        })
    
    return pd.DataFrame(users)


def generate_products(num_products=200):
    """生成商品数据"""
    products = []
    for product_id in range(1, num_products + 1):
        category = random.choice(CATEGORIES)
        product_name = f"{category}商品{product_id}"
        price = round(random.uniform(10, 5000), 2)
        stock = random.randint(0, 1000)
        
        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "price": price,
            "stock": stock
        })
    
    return pd.DataFrame(products)


def generate_orders(users_df, num_orders=5000):
    """生成订单数据"""
    orders = []
    order_items = []
    
    for order_id in range(1, num_orders + 1):
        user_id = random.choice(users_df["user_id"].tolist())
        
        # 订单日期：过去1年内随机
        days_ago = random.randint(1, 365)
        order_date = datetime.now() - timedelta(days=days_ago, 
                                                hours=random.randint(0, 23),
                                                minutes=random.randint(0, 59))
        
        # 订单状态
        status = random.choices(
            ORDER_STATUSES,
            weights=[10, 15, 20, 45, 10]  # 已完成占比最高
        )[0]
        
        # 生成订单明细（1-5个商品）
        num_items = random.randint(1, 5)
        total_amount = 0
        
        for _ in range(num_items):
            product_id = random.randint(1, 200)
            quantity = random.randint(1, 3)
            price = round(random.uniform(10, 500), 2)
            total_amount += price * quantity
            
            order_items.append({
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "price": price
            })
        
        total_amount = round(total_amount, 2)
        
        orders.append({
            "order_id": order_id,
            "user_id": user_id,
            "order_date": order_date.isoformat(),
            "total_amount": total_amount,
            "status": status
        })
    
    return pd.DataFrame(orders), pd.DataFrame(order_items)


def generate_user_behavior(users_df, products_df, num_records=50000):
    """生成用户行为日志"""
    behaviors = []
    
    for _ in range(num_records):
        user_id = random.choice(users_df["user_id"].tolist())
        product_id = random.choice(products_df["product_id"].tolist())
        behavior_type = random.choices(
            BEHAVIOR_TYPES,
            weights=[50, 20, 15, 10, 5]  # 浏览最多
        )[0]
        
        # 行为时间：过去30天内随机
        days_ago = random.randint(0, 30)
        behavior_time = datetime.now() - timedelta(
            days=days_ago,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        duration = random.randint(5, 600)  # 5秒到10分钟
        device = random.choice(DEVICES)
        channel = random.choice(CHANNELS)
        
        behaviors.append({
            "user_id": user_id,
            "product_id": product_id,
            "behavior_type": behavior_type,
            "behavior_time": behavior_time.isoformat(),
            "duration": duration,
            "device": device,
            "channel": channel
        })
    
    return pd.DataFrame(behaviors)


def generate_all_data(num_users=1000, num_products=200, num_orders=5000, num_behaviors=50000):
    """生成所有模拟数据并保存到数据库"""
    from data.database import clear_table, bulk_insert, init_database
    
    print("[START] Generating mock data...")
    
    # 初始化数据库
    init_database()
    
    # 清空现有数据
    print("[CLEAR] Clearing existing data...")
    tables = ["users", "products", "orders", "order_items", "user_behavior"]
    for table in tables:
        clear_table(table)
    
    # 生成用户数据
    print(f"[USERS] Generating {num_users} users...")
    users_df = generate_users(num_users)
    bulk_insert("users", users_df)
    
    # 生成商品数据
    print(f"[PRODUCTS] Generating {num_products} products...")
    products_df = generate_products(num_products)
    bulk_insert("products", products_df)
    
    # 生成订单数据
    print(f"[ORDERS] Generating {num_orders} orders...")
    orders_df, order_items_df = generate_orders(users_df, num_orders)
    bulk_insert("orders", orders_df)
    bulk_insert("order_items", order_items_df)
    
    # 生成用户行为数据
    print(f"[BEHAVIOR] Generating {num_behaviors} behavior logs...")
    behavior_df = generate_user_behavior(users_df, products_df, num_behaviors)
    bulk_insert("user_behavior", behavior_df)
    
    print("[OK] Data generation completed!")
    print(f"   - Users: {num_users}")
    print(f"   - Products: {num_products}")
    print(f"   - Orders: {num_orders}")
    print(f"   - Order Items: {len(order_items_df)}")
    print(f"   - Behavior Logs: {num_behaviors}")
    
    return {
        "users": users_df,
        "products": products_df,
        "orders": orders_df,
        "order_items": order_items_df,
        "behavior": behavior_df
    }


def load_sample_data():
    """加载示例数据（用于演示）"""
    from data.database import execute_query
    
    users = execute_query("SELECT * FROM users LIMIT 100")
    orders = execute_query("SELECT * FROM orders LIMIT 100")
    behavior = execute_query("SELECT * FROM user_behavior LIMIT 100")
    
    return users, orders, behavior


if __name__ == "__main__":
    # 生成模拟数据
    data = generate_all_data(
        num_users=1000,
        num_products=200,
        num_orders=5000,
        num_behaviors=50000
    )
    
    print("\n[PREVIEW] Data preview:")
    for name, df in data.items():
        print(f"\n{name}:")
        print(df.head())
