"""
购买意向预测模型 - PyTorch 二分类模型（优化版）
"""
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, f1_score, classification_report, confusion_matrix
import pandas as pd
import numpy as np
from pathlib import Path
from config.settings import MODEL_CONFIG, BASE_DIR
import matplotlib.pyplot as plt


class PurchaseIntentModel(nn.Module):
    """购买意向预测神经网络（优化版 - 带批量归一化）"""
    
    def __init__(self, input_dim, hidden_dims=[128, 64, 32], dropout_rates=[0.4, 0.3, 0.2]):
        super(PurchaseIntentModel, self).__init__()
        
        # 动态构建网络层
        layers = []
        prev_dim = input_dim
        
        for i, (hidden_dim, dropout_rate) in enumerate(zip(hidden_dims, dropout_rates)):
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))  # 批量归一化
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            prev_dim = hidden_dim
        
        # 输出层
        layers.append(nn.Linear(prev_dim, 1))
        layers.append(nn.Sigmoid())
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)


def prepare_data(df_behavior, df_orders, df_users=None, df_products=None):
    """
    准备训练数据（优化版 - 更多特征）
    特征：用户行为特征 + 用户画像特征 + 商品特征
    标签：是否购买（1=购买，0=未购买）
    """
    # 基础行为特征
    behavior_features = df_behavior.groupby("user_id").agg({
        "behavior_type": [
            lambda x: (x == "浏览").sum(),  # 浏览次数
            lambda x: (x == "加购").sum(),  # 加购次数
            lambda x: (x == "收藏").sum(),  # 收藏次数
            lambda x: (x == "购买").sum(),  # 购买次数
        ],
        "duration": ["sum", "mean", "max"],  # 时长统计
        "product_id": "nunique",  # 浏览商品数
        "category": "nunique",  # 浏览类目数
    }).reset_index()
    
    # 展平多级列名
    behavior_features.columns = [
        "user_id", "view_count", "cart_count", "favorite_count", "buy_count",
        "total_duration", "avg_duration", "max_duration",
        "product_count", "category_count"
    ]
    
    # 计算转化率特征
    behavior_features["cart_rate"] = behavior_features["cart_count"] / behavior_features["view_count"].clip(lower=1)
    behavior_features["buy_rate"] = behavior_features["buy_count"] / behavior_features["view_count"].clip(lower=1)
    behavior_features["category_diversity"] = behavior_features["category_count"] / behavior_features["product_count"].clip(lower=1)
    
    # 时间特征（如果有时间戳）
    if "timestamp" in df_behavior.columns:
        df_behavior["hour"] = pd.to_datetime(df_behavior["timestamp"]).dt.hour
        df_behavior["weekday"] = pd.to_datetime(df_behavior["timestamp"]).dt.weekday
        
        time_features = df_behavior.groupby("user_id").agg({
            "hour": ["mean", "std"],
            "weekday": ["mean", "std"],
        }).reset_index()
        
        time_features.columns = ["user_id", "avg_hour", "std_hour", "avg_weekday", "std_weekday"]
        behavior_features = behavior_features.merge(time_features, on="user_id", how="left")
    
    # 用户画像特征（如果提供）
    if df_users is not None:
        user_features = df_users[["user_id", "age", "gender", "membership_level"]].copy()
        
        # 性别编码
        user_features["gender"] = user_features["gender"].map({"男": 0, "女": 1, "未知": 2}).fillna(2)
        
        # 会员等级编码
        user_features["membership_level"] = user_features["membership_level"].map({
            "普通": 0, "银卡": 1, "金卡": 2, "钻石": 3
        }).fillna(0)
        
        behavior_features = behavior_features.merge(user_features, on="user_id", how="left")
    
    # 统计购买行为
    purchase_users = df_orders["user_id"].unique() if df_orders is not None else []
    behavior_features["purchased"] = behavior_features["user_id"].apply(
        lambda x: 1 if x in purchase_users else 0
    )
    
    # 选择特征列
    feature_cols = [
        "view_count", "cart_count", "favorite_count", "buy_count",
        "total_duration", "avg_duration", "max_duration",
        "product_count", "category_count",
        "cart_rate", "buy_rate", "category_diversity"
    ]
    
    # 添加时间特征（如果存在）
    if "avg_hour" in behavior_features.columns:
        feature_cols.extend(["avg_hour", "std_hour", "avg_weekday", "std_weekday"])
    
    # 添加用户画像特征（如果存在）
    if "age" in behavior_features.columns:
        feature_cols.extend(["age", "gender", "membership_level"])
    
    # 填充缺失值
    X = behavior_features[feature_cols].fillna(0).values
    y = behavior_features["purchased"].values
    
    return X, y, feature_cols


def train_model(X, y, epochs=None, batch_size=None, learning_rate=None, hidden_dims=[128, 64, 32]):
    """
    训练购买意向预测模型（优化版）
    返回：模型、标准化器、训练历史、评估指标
    """
    # 使用配置参数
    epochs = epochs or MODEL_CONFIG["default_epochs"]
    batch_size = batch_size or MODEL_CONFIG["batch_size"]
    learning_rate = learning_rate or MODEL_CONFIG["learning_rate"]
    
    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 划分训练集、验证集和测试集
    X_temp, X_test, y_temp, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=MODEL_CONFIG["random_state"]
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=MODEL_CONFIG["random_state"]
    )
    
    # 转换为 PyTorch 张量
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(y_train).reshape(-1, 1)
    X_val_tensor = torch.FloatTensor(X_val)
    y_val_tensor = torch.FloatTensor(y_val).reshape(-1, 1)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.FloatTensor(y_test).reshape(-1, 1)
    
    # 创建模型（优化版 - 更深层的网络）
    input_dim = X.shape[1]
    model = PurchaseIntentModel(input_dim, hidden_dims=hidden_dims)
    
    # 损失函数和优化器（添加L2正则化）
    criterion = nn.BCELoss()
    optimizer = optim.Adam(
        model.parameters(), 
        lr=learning_rate,
        weight_decay=0.001  # L2正则化防止过拟合
    )
    
    # 学习率调度器
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5, verbose=True
    )
    
    # 训练记录
    train_losses = []
    train_accuracies = []
    val_losses = []
    val_accuracies = []
    
    # 早停机制
    best_val_loss = float('inf')
    patience_counter = 0
    best_model_state = None
    
    # 训练循环
    model.train()
    for epoch in range(epochs):
        # 批量训练
        total_loss = 0
        correct = 0
        total = 0
        
        for i in range(0, len(X_train), batch_size):
            batch_X = X_train_tensor[i:i+batch_size]
            batch_y = y_train_tensor[i:i+batch_size]
            
            # 前向传播
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            # 计算准确率
            predicted = (outputs > 0.5).float()
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()
        
        avg_loss = total_loss / (len(X_train) // batch_size + 1)
        accuracy = correct / total
        
        train_losses.append(avg_loss)
        train_accuracies.append(accuracy)
        
        # 验证集评估
        model.eval()
        with torch.no_grad():
            val_outputs = model(X_val_tensor)
            val_loss = criterion(val_outputs, y_val_tensor).item()
            val_predicted = (val_outputs > 0.5).float()
            val_accuracy = (val_predicted == y_val_tensor).sum().item() / len(y_val)
        
        val_losses.append(val_loss)
        val_accuracies.append(val_accuracy)
        
        # 学习率调度
        scheduler.step(val_loss)
        
        # 早停检查
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            best_model_state = model.state_dict().copy()
        else:
            patience_counter += 1
        
        if patience_counter >= 10:  # 早停耐心值
            print(f"Early stopping at epoch {epoch+1}")
            break
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {avg_loss:.4f}, Train Acc: {accuracy:.4f}, "
                  f"Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}")
    
    # 加载最佳模型
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
    
    # 最终评估（测试集）
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        test_predicted = (test_outputs > 0.5).float()
        test_probabilities = test_outputs.numpy().flatten()
        test_labels = y_test_tensor.numpy().flatten()
        
        test_accuracy = (test_predicted == y_test_tensor).sum().item() / len(y_test)
        test_auc = roc_auc_score(test_labels, test_probabilities)
        test_f1 = f1_score(test_labels, test_predicted.numpy().flatten())
    
    # 打印详细评估报告
    print("\n" + "="*50)
    print("模型评估报告")
    print("="*50)
    print(f"测试集准确率: {test_accuracy:.4f}")
    print(f"测试集AUC: {test_auc:.4f}")
    print(f"测试集F1分数: {test_f1:.4f}")
    print("\n分类报告:")
    print(classification_report(test_labels, test_predicted.numpy().flatten()))
    print("="*50)
    
    # 保存模型
    MODEL_CONFIG["models_dir"].mkdir(parents=True, exist_ok=True)
    model_path = MODEL_CONFIG["models_dir"] / "purchase_intent_model.pth"
    torch.save({
        'model_state_dict': model.state_dict(),
        'scaler': scaler,
        'input_dim': input_dim,
        'hidden_dims': hidden_dims,
        'test_accuracy': test_accuracy,
        'test_auc': test_auc,
        'test_f1': test_f1
    }, model_path)
    
    print(f"\n✅ 模型已保存到: {model_path}")
    
    # 返回训练历史和评估指标
    history = {
        'train_losses': train_losses,
        'train_accuracies': train_accuracies,
        'val_losses': val_losses,
        'val_accuracies': val_accuracies,
        'test_accuracy': test_accuracy,
        'test_auc': test_auc,
        'test_f1': test_f1
    }
    
    return model, scaler, history


def load_model():
    """加载训练好的模型（优化版 - 支持新格式）"""
    model_path = MODEL_CONFIG["models_dir"] / "purchase_intent_model.pth"
    
    if not model_path.exists():
        print("⚠️ 模型文件不存在，请先训练模型")
        return None, None, None
    
    checkpoint = torch.load(model_path, weights_only=False, map_location=torch.device('cpu'))
    
    # 创建模型（支持新旧两种格式）
    if 'input_dim' in checkpoint:
        # 新格式
        input_dim = checkpoint['input_dim']
        hidden_dims = checkpoint.get('hidden_dims', [128, 64, 32])
        model = PurchaseIntentModel(input_dim, hidden_dims=hidden_dims)
    else:
        # 旧格式兼容
        input_dim = len(checkpoint.get('features', []))
        model = PurchaseIntentModel(input_dim)
    
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    scaler = checkpoint['scaler']
    
    # 加载评估指标（如果有）
    metrics = None
    if 'test_accuracy' in checkpoint:
        metrics = {
            'test_accuracy': checkpoint.get('test_accuracy'),
            'test_auc': checkpoint.get('test_auc'),
            'test_f1': checkpoint.get('test_f1')
        }
        print(f"✅ 模型已从 {model_path} 加载")
        print(f"   测试准确率: {metrics['test_accuracy']:.4f}")
        print(f"   测试AUC: {metrics['test_auc']:.4f}")
        print(f"   测试F1分数: {metrics['test_f1']:.4f}")
    else:
        print(f"✅ 模型已从 {model_path} 加载")
    
    return model, scaler, metrics


def predict_purchase_intent(model, scaler, user_features):
    """
    预测用户购买意向（优化版 - 返回概率和类别）
    """
    # 标准化特征
    features_scaled = scaler.transform(user_features)
    
    # 转换为张量
    X_tensor = torch.FloatTensor(features_scaled)
    
    # 预测
    model.eval()
    with torch.no_grad():
        predictions = model(X_tensor)
        probabilities = predictions.numpy().flatten()
        predicted_classes = (probabilities > 0.5).astype(int)
    
    return probabilities, predicted_classes


def plot_training_history(history):
    """
    绘制训练历史（损失和准确率曲线）
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # 损失曲线
    axes[0].plot(history['train_losses'], label='训练损失')
    if 'val_losses' in history and len(history['val_losses']) > 0:
        axes[0].plot(history['val_losses'], label='验证损失')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('训练和验证损失')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 准确率曲线
    axes[1].plot(history['train_accuracies'], label='训练准确率')
    if 'val_accuracies' in history and len(history['val_accuracies']) > 0:
        axes[1].plot(history['val_accuracies'], label='验证准确率')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy')
    axes[1].set_title('训练和验证准确率')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    # 测试代码
    from data.database import execute_query
    
    print("正在加载数据...")
    behavior_data = execute_query("SELECT * FROM user_behavior LIMIT 10000")
    orders_data = execute_query("SELECT * FROM orders")
    users_data = execute_query("SELECT * FROM users LIMIT 1000")
    
    if behavior_data.empty or orders_data.empty:
        print("⚠️ 数据不足，请先生成模拟数据")
    else:
        print("开始训练购买意向预测模型（优化版）...")
        X, y, features = prepare_data(behavior_data, orders_data, users_data)
        print(f"特征维度: {X.shape[1]}, 特征列表: {features}")
        model, scaler, history = train_model(X, y, hidden_dims=[128, 64, 32])
        print(f"\n训练完成！")
        print(f"测试准确率: {history['test_accuracy']:.4f}")
        print(f"测试AUC: {history['test_auc']:.4f}")
        print(f"测试F1分数: {history['test_f1']:.4f}")
        
        # 绘制训练历史
        fig = plot_training_history(history)
        plt.savefig("training_history.png")
        print("训练历史图已保存到 training_history.png")
