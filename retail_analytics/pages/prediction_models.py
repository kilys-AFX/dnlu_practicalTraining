"""
预测模型模块 - 购买意向预测 & 销售预测
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from data.database import execute_query
from config.settings import MODEL_CONFIG


def show_purchase_intent_page():
    """购买意向预测页面（优化版）"""
    st.markdown("## 🎯 购买意向预测")
    
    # 检查模型是否存在
    model_path = MODEL_CONFIG["models_dir"] / "purchase_intent_model.pth"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 模型训练（优化版）")
        
        # 训练参数设置
        st.markdown("#### 训练参数")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            epochs = st.slider("训练轮次", min_value=10, max_value=200, value=50)
        with col_b:
            hidden_layer1 = st.slider("隐藏层1维度", min_value=64, max_value=256, value=128, step=32)
        with col_c:
            hidden_layer2 = st.slider("隐藏层2维度", min_value=32, max_value=128, value=64, step=16)
        
        hidden_dims = [hidden_layer1, hidden_layer2, 32]
        
        if st.button("🚀 训练模型（优化版）", type="primary", use_container_width=True):
            with st.spinner("正在训练购买意向预测模型（优化版）..."):
                try:
                    from models.purchase_intent import train_model, prepare_data, plot_training_history
                    import matplotlib.pyplot as plt
                    
                    # 加载数据
                    behavior_data = execute_query("SELECT * FROM user_behavior LIMIT 10000")
                    orders_data = execute_query("SELECT * FROM orders")
                    users_data = execute_query("SELECT * FROM users LIMIT 1000")
                    products_data = execute_query("SELECT * FROM products")
                    
                    if behavior_data.empty or orders_data.empty:
                        st.warning("⚠️ 数据不足，请先生成模拟数据。")
                    else:
                        # 准备数据（使用优化版的特征工程）
                        X, y, features = prepare_data(behavior_data, orders_data, users_data, products_data)
                        
                        st.info(f"特征维度: {X.shape[1]}, 特征数量: {len(features)}")
                        
                        # 训练模型（使用优化版的train_model）
                        model, scaler, history = train_model(X, y, epochs=epochs, hidden_dims=hidden_dims)
                        
                        # 显示评估指标
                        st.success(f"✅ 模型训练成功！")
                        col_m1, col_m2, col_m3 = st.columns(3)
                        with col_m1:
                            st.metric("测试准确率", f"{history['test_accuracy']:.4f}")
                        with col_m2:
                            st.metric("测试AUC", f"{history['test_auc']:.4f}")
                        with col_m3:
                            st.metric("测试F1分数", f"{history['test_f1']:.4f}")
                        
                        # 绘制训练历史
                        fig = plot_training_history(history)
                        st.pyplot(fig)
                        plt.close()
                        
                except Exception as e:
                    st.error(f"❌ 训练失败: {str(e)}")
    
    with col2:
        st.markdown("### 📈 模型信息（优化版）")
        
        if model_path.exists():
            st.success("✅ 模型文件已存在")
            
            # 加载并显示模型信息
            try:
                from models.purchase_intent import load_model
                
                model, scaler, metrics = load_model()
                
                if metrics:
                    st.info(f"测试准确率: {metrics['test_accuracy']:.4f}")
                    st.info(f"测试AUC: {metrics['test_auc']:.4f}")
                    st.info(f"测试F1分数: {metrics['test_f1']:.4f}")
                else:
                    st.warning("模型格式较旧，建议重新训练")
                    
            except Exception as e:
                st.warning(f"无法加载模型信息: {e}")
        else:
            st.warning("⚠️ 模型尚未训练")
    
    # 预测部分（优化版 - 更多特征）
    st.markdown("### 🔮 进行预测（优化版）")
    
    if model_path.exists():
        with st.form("prediction_form"):
            st.markdown("请输入用户行为特征（优化版）：")
            
            # 基础特征
            st.markdown("##### 基础行为特征")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                view_count = st.number_input("浏览次数", min_value=0, value=10)
                cart_count = st.number_input("加购次数", min_value=0, value=2)
            
            with col2:
                total_duration = st.number_input("总时长（秒）", min_value=0, value=300)
                avg_duration = st.number_input("平均时长（秒）", min_value=0, value=60)
            
            with col3:
                product_count = st.number_input("商品数量", min_value=0, value=5)
                category_count = st.number_input("类目数量", min_value=0, value=3)
            
            with col4:
                max_duration = st.number_input("最大时长（秒）", min_value=0, value=120)
                buy_rate = st.number_input("购买率", min_value=0.0, max_value=1.0, value=0.1)
            
            submitted = st.form_submit_button("预测购买意向（优化版）")
            
            if submitted:
                try:
                    from models.purchase_intent import load_model, predict_purchase_intent
                    import numpy as np
                    
                    model, scaler, metrics = load_model()
                    
                    if model is not None:
                        # 构建特征向量（需要根据实际训练时的特征顺序）
                        user_features = np.array([[
                            view_count, cart_count, 0, 0,  # 假设favorite_count和buy_count为0
                            total_duration, avg_duration, max_duration,
                            product_count, category_count,
                            cart_count/view_count if view_count > 0 else 0, buy_rate,  # cart_rate和buy_rate
                            category_count/product_count if product_count > 0 else 0  # category_diversity
                        ]])
                        
                        # 如果特征维度不匹配，使用简单版本
                        if user_features.shape[1] != scaler.n_features_in_:
                            st.warning(f"特征维度不匹配：输入{user_features.shape[1]}，期望{scaler.n_features_in_}。使用简化版本。")
                            user_features = np.array([[view_count, total_duration, product_count, avg_duration]])
                        
                        probabilities, predicted_classes = predict_purchase_intent(model, scaler, user_features)
                        
                        # 显示预测结果
                        st.success(f"🎯 购买概率: **{probabilities[0]:.2%}**")
                        
                        if predicted_classes[0] == 1:
                            st.success("✅ 高购买意向！")
                        else:
                            st.info("ℹ️ 低购买意向")
                            
                        # 显示置信度
                        confidence = abs(probabilities[0] - 0.5) * 2
                        st.progress(probabilities[0])
                        st.caption(f"置信度: {confidence:.2%}")
                        
                except Exception as e:
                    st.error(f"❌ 预测失败: {str(e)}")
    else:
        st.info("ℹ️ 请先训练模型以进行预测。")


def show_sales_forecast_page():
    """销售预测页面 (LSTM)"""
    st.markdown("## 📈 销售预测 (LSTM)")
    
    # 检查模型是否存在
    model_path = MODEL_CONFIG["models_dir"] / "lstm_sales_model.pth"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 模型训练")
        
        # 训练参数
        seq_length = st.slider("序列长度（天）", min_value=5, max_value=30, value=10)
        epochs = st.slider("训练轮次", min_value=10, max_value=200, value=50)
        
        if st.button("🚀 训练LSTM模型", type="primary", use_container_width=True):
            with st.spinner("正在训练LSTM销售预测模型..."):
                try:
                    from models.sales_forecast import train_lstm_model, prepare_sales_data
                    
                    # 加载数据
                    orders_data = execute_query("""
                    SELECT order_date, total_amount
                    FROM orders
                    WHERE status != 'Cancelled'
                    ORDER BY order_date
                    """)
                    
                    if orders_data.empty:
                        st.warning("⚠️ 数据不足，请先生成模拟数据。")
                    else:
                        # 准备数据
                        dates, values = prepare_sales_data(orders_data)
                        
                        # 训练模型
                        model, scaler, losses, predictions, actuals = train_lstm_model(
                            dates, values, seq_length=seq_length, epochs=epochs
                        )
                        
                        st.success("✅ 模型训练成功！")
                        
                        # 绘制训练损失曲线
                        fig1 = px.line(
                            x=list(range(1, len(losses) + 1)),
                            y=losses,
                            title="训练损失曲线",
                            labels={"x": "训练轮次", "y": "损失值"}
                        )
                        st.plotly_chart(fig1, use_container_width=True)
                        
                        # 绘制预测值与真实值对比
                        fig2 = px.line(
                            title="预测值 vs 真实值 (测试集)",
                            labels={"value": "销售额", "index": "样本"}
                        )
                        fig2.add_scatter(y=actuals.flatten(), name="真实值")
                        fig2.add_scatter(y=predictions.flatten(), name="预测值")
                        st.plotly_chart(fig2, use_container_width=True)
                        
                except Exception as e:
                    st.error(f"❌ 训练失败: {str(e)}")
    
    with col2:
        st.markdown("### 📈 模型信息")
        
        if model_path.exists():
            st.success("✅ 模型文件已存在")
        else:
            st.warning("⚠️ 模型尚未训练")
    
    # 预测部分
    st.markdown("### 🔮 未来预测")
    
    if model_path.exists():
        n_future = st.slider("预测天数", min_value=1, max_value=30, value=7)
        
        if st.button("生成预测", type="secondary", use_container_width=True):
            with st.spinner("正在生成预测..."):
                try:
                    from models.sales_forecast import load_lstm_model, predict_future_sales
                    
                    model, scaler, seq_length = load_lstm_model()
                    
                    if model is not None:
                        # 从数据库获取最后序列
                        orders_data = execute_query("""
                        SELECT SUM(total_amount) as daily_sales
                        FROM orders
                        WHERE status != 'Cancelled'
                        GROUP BY DATE(order_date)
                        ORDER BY order_date DESC
                        LIMIT ?
                        """, (seq_length,))
                        
                        if len(orders_data) == seq_length:
                            import numpy as np
                            last_sequence = scaler.transform(orders_data["daily_sales"].values.reshape(-1, 1)).flatten()
                            
                            # 预测未来销售
                            future_sales = predict_future_sales(model, scaler, last_sequence, seq_length, n_future)
                            
                            # 显示预测结果
                            forecast_df = pd.DataFrame({
                                "天数": list(range(1, n_future + 1)),
                                "预测销售额": future_sales
                            })
                            
                            st.success("✅ 预测生成成功！")
                            st.dataframe(forecast_df, use_container_width=True)
                            
                            # 绘制预测图表
                            fig = px.line(
                                forecast_df,
                                x="天数",
                                y="预测销售额",
                                title=f"销售预测 (未来 {n_future} 天)",
                                markers=True
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning(f"⚠️ 需要至少 {seq_length} 天的数据进行预测")
                except Exception as e:
                    st.error(f"❌ 预测失败: {str(e)}")
    else:
        st.info("ℹ️ 请先训练模型以生成预测。")


if __name__ == "__main__":
    show_purchase_intent_page()
