"""
销量预测模型 - LSTM 时间序列预测
"""
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from pathlib import Path
from config.settings import MODEL_CONFIG, BASE_DIR


class LSTMSalesForecast(nn.Module):
    """LSTM 销量预测模型"""
    
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1):
        super(LSTMSalesForecast, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True,
            dropout=0.2 if num_layers > 1 else 0
        )
        
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        # 初始化隐藏状态
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        # LSTM 层
        out, _ = self.lstm(x, (h0, c0))
        
        # 只取最后一个时间步的输出
        out = self.fc(out[:, -1, :])
        
        return out


def create_sequences(data, seq_length=10):
    """
    创建时间序列样本
    参数：
        data: 时间序列数据
        seq_length: 序列长度（用过去多少天预测下一天）
    返回：
        X: 输入序列 (n_samples, seq_length, 1)
        y: 输出值 (n_samples, 1)
    """
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    
    return np.array(X), np.array(y)


def prepare_sales_data(df_orders, date_col="order_date", target_col="total_amount", freq="D"):
    """
    准备销量预测数据
    参数：
        df_orders: 订单数据框
        date_col: 日期列名
        target_col: 目标列名（如销量或销售额）
        freq: 聚合频率 ('D'=天, 'W'=周, 'M'=月)
    返回：
        dates: 日期列表
        values: 聚合后的数值列表
    """
    # 转换日期格式
    df_orders[date_col] = pd.to_datetime(df_orders[date_col])
    
    # 按日期聚合
    if freq == "D":
        df_orders["date"] = df_orders[date_col].dt.date
    elif freq == "W":
        df_orders["date"] = df_orders[date_col].dt.to_period("W").apply(lambda x: x.start_time.date())
    elif freq == "M":
        df_orders["date"] = df_orders[date_col].dt.to_period("M").apply(lambda x: x.start_time.date())
    
    # 聚合目标值
    daily_data = df_orders.groupby("date")[target_col].sum().reset_index()
    daily_data.columns = ["date", "value"]
    
    # 填充缺失日期
    all_dates = pd.date_range(
        start=daily_data["date"].min(),
        end=daily_data["date"].max(),
        freq=freq
    )
    
    all_dates_df = pd.DataFrame({"date": all_dates.date})
    daily_data = all_dates_df.merge(daily_data, on="date", how="left").fillna(0)
    
    return daily_data["date"].tolist(), daily_data["value"].tolist()


def train_lstm_model(dates, values, seq_length=10, epochs=None, batch_size=None, learning_rate=None):
    """
    训练 LSTM 销量预测模型
    参数：
        dates: 日期列表
        values: 销量/销售额列表
        seq_length: 序列长度
        epochs: 训练轮数
        batch_size: 批次大小
        learning_rate: 学习率
    返回：
        model: 训练好的模型
        scaler: 数据标准化器
        losses: 训练损失历史
        predictions: 预测结果
        actuals: 实际值
    """
    # 使用配置参数
    epochs = epochs or MODEL_CONFIG["default_epochs"]
    batch_size = batch_size or MODEL_CONFIG["batch_size"]
    learning_rate = learning_rate or MODEL_CONFIG["learning_rate"]
    
    # 数据标准化
    scaler = MinMaxScaler(feature_range=(0, 1))
    values_scaled = scaler.fit_transform(np.array(values).reshape(-1, 1))
    
    # 创建序列数据
    X, y = create_sequences(values_scaled, seq_length)
    
    # 划分训练集和测试集
    train_size = int(len(X) * (1 - MODEL_CONFIG["test_size"]))
    
    X_train = X[:train_size]
    y_train = y[:train_size]
    X_test = X[train_size:]
    y_test = y[train_size:]
    
    # 转换为 PyTorch 张量
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(y_train).reshape(-1, 1)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.FloatTensor(y_test).reshape(-1, 1)
    
    # 创建 LSTM 模型
    input_size = 1  # 单变量时间序列
    hidden_size = 64
    num_layers = 2
    output_size = 1
    
    model = LSTMSalesForecast(input_size, hidden_size, num_layers, output_size)
    
    # 损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # 训练记录
    losses = []
    
    # 训练循环
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        
        # 批量训练
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
        
        avg_loss = total_loss / (len(X_train) // batch_size + 1)
        losses.append(avg_loss)
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.6f}")
    
    # 评估模型
    model.eval()
    with torch.no_grad():
        predictions_scaled = model(X_test_tensor).numpy()
    
    # 反标准化
    predictions = scaler.inverse_transform(predictions_scaled)
    actuals = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    # 计算评估指标
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    mae = mean_absolute_error(actuals, predictions)
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    
    print(f"\n✅ 模型训练完成！")
    print(f"   MAE: {mae:.2f}")
    print(f"   RMSE: {rmse:.2f}")
    
    # 保存模型
    MODEL_CONFIG["models_dir"].mkdir(parents=True, exist_ok=True)
    model_path = MODEL_CONFIG["models_dir"] / "lstm_sales_model.pth"
    torch.save({
        'model_state_dict': model.state_dict(),
        'scaler': scaler,
        'seq_length': seq_length,
        'input_size': input_size,
        'hidden_size': hidden_size,
        'num_layers': num_layers,
    }, model_path)
    
    print(f"✅ 模型已保存到: {model_path}")
    
    return model, scaler, losses, predictions, actuals


def load_lstm_model():
    """加载训练好的 LSTM 模型"""
    model_path = MODEL_CONFIG["models_dir"] / "lstm_sales_model.pth"
    
    if not model_path.exists():
        print("⚠️ 模型文件不存在，请先训练模型")
        return None, None
    
    checkpoint = torch.load(model_path, weights_only=False)
    
    # 创建模型
    model = LSTMSalesForecast(
        checkpoint['input_size'],
        checkpoint['hidden_size'],
        checkpoint['num_layers'],
        1
    )
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    scaler = checkpoint['scaler']
    seq_length = checkpoint['seq_length']
    
    print(f"✅ 模型已从 {model_path} 加载")
    print(f"   序列长度: {seq_length}")
    
    return model, scaler, seq_length


def predict_future_sales(model, scaler, last_sequence, seq_length, n_future=7):
    """
    预测未来销量
    参数：
        model: 训练好的 LSTM 模型
        scaler: 数据标准化器
        last_sequence: 最后一段序列数据（已标准化）
        seq_length: 序列长度
        n_future: 预测未来多少天
    返回：
        future_predictions: 未来销量预测值（反标准化）
    """
    model.eval()
    with torch.no_grad():
        # 复制最后一段序列
        current_seq = last_sequence.copy()
        future_predictions = []
        
        for _ in range(n_future):
            # 转换为张量
            seq_tensor = torch.FloatTensor(current_seq).reshape(1, seq_length, 1)
            
            # 预测
            pred_scaled = model(seq_tensor).numpy()[0, 0]
            
            # 保存预测结果
            future_predictions.append(pred_scaled)
            
            # 更新序列（滑动窗口）
            current_seq = np.roll(current_seq, -1)
            current_seq[-1] = pred_scaled
        
        # 反标准化
        future_predictions = scaler.inverse_transform(
            np.array(future_predictions).reshape(-1, 1)
        ).flatten()
    
    return future_predictions


if __name__ == "__main__":
    # 测试代码
    from data.database import execute_query
    
    print("正在加载数据...")
    orders_data = execute_query("""
    SELECT order_date, total_amount
    FROM orders
    WHERE status != '已取消'
    ORDER BY order_date
    """)
    
    if orders_data.empty:
        print("⚠️ 数据不足，请先生成模拟数据")
    else:
        print("开始训练 LSTM 销量预测模型...")
        dates, values = prepare_sales_data(orders_data)
        model, scaler, losses, predictions, actuals = train_lstm_model(dates, values, seq_length=10)
        print(f"\n训练完成！预测样本数: {len(predictions)}")
