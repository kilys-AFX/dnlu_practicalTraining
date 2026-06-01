"""
性能优化模块 - 缓存、数据库优化、性能监控
"""
import streamlit as st
import sqlite3
import time
import functools
from pathlib import Path
from config.settings import DATABASE_PATH, MODEL_CONFIG


# 缓存装饰器
def cache_data(ttl=3600):
    """
    数据缓存装饰器
    ttl: 缓存生存时间（秒），默认1小时
    """
    def decorator(func):
        @functools.lru_cache(maxsize=128)
        def cached_func(*args, **kwargs):
            return func(*args, **kwargs)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 检查缓存
            if cache_key in st.session_state:
                cache_time, cache_value = st.session_state[cache_key]
                if time.time() - cache_time < ttl:
                    return cache_value
            
            # 执行函数
            result = cached_func(*args, **kwargs)
            
            # 保存到缓存
            st.session_state[cache_key] = (time.time(), result)
            
            return result
        
        return wrapper
    return decorator


def optimize_database():
    """
    优化数据库性能
    启用WAL模式、设置缓存大小等
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        
        # 启用WAL模式（提高并发性能）
        conn.execute("PRAGMA journal_mode=WAL")
        
        # 设置同步模式为NORMAL（提高写入性能）
        conn.execute("PRAGMA synchronous=NORMAL")
        
        # 设置缓存大小（10MB）
        conn.execute("PRAGMA cache_size=-10000")
        
        # 启用外键约束
        conn.execute("PRAGMA foreign_keys=ON")
        
        # 设置临时文件存储为内存
        conn.execute("PRAGMA temp_store=MEMORY")
        
        # 设置页面大小
        conn.execute("PRAGMA page_size=4096")
        
        conn.close()
        
        print("✅ 数据库优化完成")
        return True
    except Exception as e:
        print(f"❌ 数据库优化失败: {str(e)}")
        return False


def get_database_stats():
    """
    获取数据库统计信息
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        stats = {}
        
        # 获取所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            
            # 获取表的行数
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            
            # 获取表的大小
            cursor.execute(f"SELECT SUM(pgsize) FROM dbstat WHERE name='{table_name}'")
            size_result = cursor.fetchone()[0]
            size_mb = (size_result or 0) / 1024 / 1024
            
            stats[table_name] = {
                'rows': row_count,
                'size_mb': round(size_mb, 2)
            }
        
        conn.close()
        
        return stats
    except Exception as e:
        print(f"❌ 获取数据库统计信息失败: {str(e)}")
        return None


def optimize_model_loading():
    """
    优化模型加载性能
    使用单例模式，避免重复加载
    """
    if 'models' not in st.session_state:
        st.session_state.models = {}
    
    def load_model_cached(model_name):
        """加载模型（带缓存）"""
        if model_name in st.session_state.models:
            return st.session_state.models[model_name]
        
        # 加载模型
        if model_name == 'purchase_intent':
            from models.purchase_intent import load_model
            model, scaler, metrics = load_model()
            model_data = {
                'model': model,
                'scaler': scaler,
                'metrics': metrics
            }
        
        elif model_name == 'sales_forecast':
            # 销售预测模型加载
            model_data = None  # 待实现
        
        else:
            raise ValueError(f"未知的模型: {model_name}")
        
        # 缓存模型
        if model_data and model_data.get('model') is not None:
            st.session_state.models[model_name] = model_data
        
        return model_data
    
    return load_model_cached


def measure_performance(func):
    """
    性能测量装饰器
    测量函数执行时间
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 记录性能数据
        if 'performance_log' not in st.session_state:
            st.session_state.performance_log = []
        
        st.session_state.performance_log.append({
            'function': func.__name__,
            'execution_time': execution_time,
            'timestamp': time.time()
        })
        
        # 只保留最近100条记录
        if len(st.session_state.performance_log) > 100:
            st.session_state.performance_log = st.session_state.performance_log[-100:]
        
        return result
    
    return wrapper


def show_performance_dashboard():
    """
    显示性能监控仪表板
    """
    st.markdown("### 📊 性能监控")
    
    # 数据库统计
    st.markdown("#### 数据库统计")
    db_stats = get_database_stats()
    
    if db_stats:
        total_rows = sum(stat['rows'] for stat in db_stats.values())
        total_size_mb = sum(stat['size_mb'] for stat in db_stats.values())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总表数", len(db_stats))
        with col2:
            st.metric("总行数", f"{total_rows}")
        with col3:
            st.metric("总大小", f"{total_size_mb:.2f} MB")
        
        # 显示各表统计
        for table_name, stats in db_stats.items():
            with st.expander(f"表: {table_name}"):
                st.write(f"**行数**: {stats['rows']}")
                st.write(f"**大小**: {stats['size_mb']:.2f} MB")
    
    # 性能日志
    st.markdown("#### 性能日志")
    
    if 'performance_log' in st.session_state and st.session_state.performance_log:
        log_df = pd.DataFrame(st.session_state.performance_log)
        
        # 计算平均执行时间
        avg_time = log_df['execution_time'].mean()
        max_time = log_df['execution_time'].max()
        min_time = log_df['execution_time'].min()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("平均执行时间", f"{avg_time:.3f}s")
        with col2:
            st.metric("最大执行时间", f"{max_time:.3f}s")
        with col3:
            st.metric("最小执行时间", f"{min_time:.3f}s")
        
        # 显示最近的性能日志
        st.markdown("**最近的性能日志**")
        st.dataframe(log_df.tail(10), use_container_width=True)
    else:
        st.info("暂无性能日志")
    
    # 缓存管理
    st.markdown("#### 缓存管理")
    
    if st.button("清除所有缓存"):
        # 清除Streamlit缓存
        st.cache_data.clear()
        st.cache_resource.clear()
        
        # 清除自定义缓存
        keys_to_remove = [key for key in st.session_state.keys() if key.startswith('cache_')]
        for key in keys_to_remove:
            del st.session_state[key]
        
        st.success("✅ 所有缓存已清除")
    
    # 数据库优化
    st.markdown("#### 数据库优化")
    
    if st.button("优化数据库性能"):
        with st.spinner("正在优化数据库..."):
            if optimize_database():
                st.success("✅ 数据库优化完成")
            else:
                st.error("❌ 数据库优化失败")


# 初始化性能优化
def init_performance_optimization():
    """初始化性能优化"""
    # 优化数据库
    optimize_database()
    
    # 预热模型（可选）
    if MODEL_CONFIG.get('preload_models', False):
        optimize_model_loading()()


if __name__ == "__main__":
    # 测试代码
    print("测试性能优化模块...")
    
    # 测试数据库优化
    optimize_database()
    
    # 测试获取数据库统计
    stats = get_database_stats()
    if stats:
        print("数据库统计信息:")
        for table, stat in stats.items():
            print(f"  {table}: {stat['rows']} 行, {stat['size_mb']} MB")
    
    print("✅ 性能优化模块测试完成")