"""
智能零售用户行为分析系统 - 主入口
"""
import streamlit as st
import streamlit_antd_components as sac
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# 导入认证模块
from utils.auth import init_auth_db, authenticate_user, get_user_by_id, update_last_login, check_permission, create_user

# Import config
from config.settings import APP_CONFIG

# 导入性能优化模块
from utils.performance import init_performance_optimization, show_performance_dashboard

# Set page config
st.set_page_config(
    page_title=APP_CONFIG["title"],
    page_icon=APP_CONFIG["icon"],
    layout=APP_CONFIG["layout"],
    initial_sidebar_state=APP_CONFIG["initial_sidebar_state"]
)

# Custom CSS
def load_css():
    """加载自定义CSS"""
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background: white;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Sidebar navigation
def sidebar_navigation():
    """侧边栏导航菜单"""
    with st.sidebar:
        # 显示用户信息
        if st.session_state.user:
            user = st.session_state.user
            st.markdown(f"## 欢迎, {user['username']}")
            st.caption(f"角色: {user['role']}")
            if st.button("登出", key="logout_btn", use_container_width=True):
                st.session_state.user = None
                st.rerun()
            st.markdown("---")
        
        st.markdown(f"## {APP_CONFIG['icon']} {APP_CONFIG['title']}")
        st.markdown("---")
        
        # Navigation menu with permission control
        menu_items = [
            sac.MenuItem("数据管理", icon="database", children=[
                sac.MenuItem("数据上传", icon="upload"),
                sac.MenuItem("数据预览", icon="eye"),
                sac.MenuItem("数据清洗", icon="sparkles"),
            ]),
            sac.MenuItem("数据概览", icon="bar-chart", children=[
                sac.MenuItem("核心指标", icon="dashboard"),
                sac.MenuItem("趋势分析", icon="trending-up"),
                sac.MenuItem("用户画像", icon="pie-chart"),
            ]),
            sac.MenuItem("行为分析", icon="activity", children=[
                sac.MenuItem("活跃度热力图", icon="heatmap"),
                sac.MenuItem("转化漏斗", icon="filter"),
                sac.MenuItem("留存分析", icon="repeat"),
                sac.MenuItem("行为路径", icon="git-branch"),
            ]),
        ]
        
        # 用户画像模块 - 所有登录用户可访问
        menu_items.append(
            sac.MenuItem("用户画像", icon="users", children=[
                sac.MenuItem("用户聚类", icon="cluster"),
                sac.MenuItem("生命周期", icon="clock"),
            ])
        )
        
        # 预测模型 - 需要user角色以上
        if check_permission(st.session_state.user['role'], 'user'):
            menu_items.append(
                sac.MenuItem("预测模型", icon="brain", children=[
                    sac.MenuItem("购买意向", icon="target"),
                    sac.MenuItem("销售预测", icon="trending-up"),
                ])
            )
        
        # 实时监控 - 需要user角色以上
        if check_permission(st.session_state.user['role'], 'user'):
            menu_items.append(
                sac.MenuItem("实时监控", icon="monitor", children=[
                    sac.MenuItem("数据大屏", icon="tv"),
                    sac.MenuItem("异常检测", icon="alert-triangle"),
                ])
            )
        
        # AI助手 - 需要manager角色以上
        if check_permission(st.session_state.user['role'], 'manager'):
            menu_items.append(
                sac.MenuItem("AI助手", icon="robot", children=[
                    sac.MenuItem("智能问答", icon="message-circle"),
                    sac.MenuItem("报告生成", icon="file-text"),
                    sac.MenuItem("PDF导出", icon="file"),
                ])
            )
        
        # 数据集成 - 需要manager角色以上
        if check_permission(st.session_state.user['role'], 'manager'):
            menu_items.append(
                sac.MenuItem("数据集成", icon="database-add", children=[
                    sac.MenuItem("CSV文件", icon="file-text"),
                    sac.MenuItem("Excel文件", icon="file-excel"),
                    sac.MenuItem("API接口", icon="cloud"),
                ])
            )
        
        # 系统管理 - 仅admin可访问
        if check_permission(st.session_state.user['role'], 'admin'):
            menu_items.append(
                sac.MenuItem("系统管理", icon="settings", children=[
                    sac.MenuItem("用户管理", icon="people"),
                    sac.MenuItem("系统日志", icon="journal-text"),
                    sac.MenuItem("性能监控", icon="speedometer"),
                ])
            )
        
        selected = sac.menu(
            items=menu_items,
            open_all=True,
            return_index=False,
        )
        
        st.markdown("---")
        
        # Data generation button - 需要manager角色以上
        if check_permission(st.session_state.user['role'], 'manager'):
            if st.button("生成模拟数据", use_container_width=True):
                with st.spinner("正在生成模拟数据..."):
                    from data.data_generator import generate_all_data
                    generate_all_data()
                    st.success("✅ 模拟数据生成成功！")
                    st.rerun()
        
        # About info
        st.markdown("### 关于")
        st.caption("版本: 3.0.0")
        st.caption("开发者: AI研究生")
    
    return selected

# Login check
def check_login():
    """检查用户登录状态"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if st.session_state.user is None:
        show_login_page()
        return False
    return True

def show_login_page():
    """显示登录页面"""
    st.markdown('<h1 class="main-header">智能零售用户行为分析系统</h1>', unsafe_allow_html=True)
    
    st.markdown("### 用户登录")
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("用户名", placeholder="请输入用户名")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            submit = st.form_submit_button("登录")
            
            if submit:
                if not username or not password:
                    st.error("请输入用户名和密码")
                else:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.user = user
                        update_last_login(user['id'])
                        st.success("登录成功！")
                        st.rerun()
                    else:
                        st.error("用户名或密码错误")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 注册新用户（管理员功能）
    if st.checkbox("注册新用户（需要管理员权限）"):
        with st.expander("用户注册"):
            with st.form("register_form"):
                new_username = st.text_input("新用户名")
                new_password = st.text_input("新密码", type="password")
                confirm_password = st.text_input("确认密码", type="password")
                email = st.text_input("邮箱")
                role = st.selectbox("角色", ["user", "manager", "admin"])
                
                if st.form_submit_button("注册"):
                    if new_password != confirm_password:
                        st.error("两次输入的密码不一致")
                    elif len(new_password) < 6:
                        st.error("密码长度至少6位")
                    else:
                        if create_user(new_username, new_password, email, role):
                            st.success("用户注册成功！")
                        else:
                            st.error("用户名已存在")

# Page routing
def main():
    """主函数"""
    # 初始化认证数据库
    init_auth_db()
    
    # 检查登录状态
    if not check_login():
        return
    
    # Sidebar navigation
    selected = sidebar_navigation()
    
    # Route to selected page
    if selected is None or "数据上传" in str(selected):
        show_data_upload()
    elif "数据预览" in str(selected):
        show_data_preview()
    elif "数据清洗" in str(selected):
        show_data_clean()
    elif "核心指标" in str(selected):
        show_key_metrics()
    elif "趋势分析" in str(selected):
        show_trend_analysis()
    elif "用户画像" in str(selected):
        show_user_portrait()
    elif "活跃度热力图" in str(selected):
        show_heatmap()
    elif "转化漏斗" in str(selected):
        show_funnel()
    elif "留存分析" in str(selected):
        show_retention()
    elif "行为路径" in str(selected):
        show_behavior_path()
    elif "用户聚类" in str(selected):
        show_clustering()
    elif "生命周期" in str(selected):
        show_lifecycle()
    elif "购买意向" in str(selected):
        show_purchase_intent()
    elif "销售预测" in str(selected):
        show_sales_forecast()
    elif "数据大屏" in str(selected):
        show_realtime_dashboard()
    elif "异常检测" in str(selected):
        show_anomaly_detection()
    elif "智能问答" in str(selected):
        show_ai_chat()
    elif "报告生成" in str(selected):
        show_report_generation()
    elif "PDF导出" in str(selected):
        show_pdf_export()
    elif "用户管理" in str(selected):
        show_user_management()
    elif "系统日志" in str(selected):
        show_system_logs()
    # 数据集成页面路由
    elif "CSV文件" in str(selected):
        show_csv_import()
    elif "Excel文件" in str(selected):
        show_excel_import()
    elif "API接口" in str(selected):
        show_api_import()
    # 性能监控
    elif "性能监控" in str(selected):
        show_performance_monitor()
    else:
        show_home()

def show_home():
    """首页"""
    st.markdown('<h1 class="main-header">智能零售用户行为分析系统</h1>', unsafe_allow_html=True)
    
    st.markdown("### 欢迎使用")
    st.markdown("""
    本系统采用 **AI驱动**，提供以下核心功能：
    
    - **数据管理**: 上传、预览、清洗数据
    - **数据概览**: 核心指标、趋势分析、用户画像
    - **行为分析**: 活跃度热力图、转化漏斗、留存分析
    - **用户画像**: 用户聚类、生命周期管理
    - **预测模型**: 购买意向预测、销售预测 (LSTM)
    - **实时监控**: 数据大屏、异常检测
    - **AI助手**: 智能问答、自动化报告生成
    
    **快速开始**:
    1. 点击 "生成模拟数据" 按钮创建测试数据
    2. 导航到不同模块开始分析
    """)
    
    # Feature cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("数据管理")
        st.caption("上传和管理您的数据")
    
    with col2:
        st.success("行为分析")
        st.caption("深度分析用户行为")
    
    with col3:
        st.warning("预测模型")
        st.caption("AI驱动的预测分析")
    
    with col4:
        st.error("实时监控")
        st.caption("实时数据监控")

# Import page functions
def show_data_upload():
    """Data upload page"""
    from pages.data_management import show_data_upload_page
    show_data_upload_page()

def show_data_preview():
    """Data preview page"""
    from pages.data_management import show_data_preview_page
    show_data_preview_page()

def show_data_clean():
    """Data clean page"""
    from pages.data_management import show_data_clean_page
    show_data_clean_page()

def show_key_metrics():
    """Key metrics page"""
    from pages.data_overview import show_key_metrics_page
    show_key_metrics_page()

def show_trend_analysis():
    """Trend analysis page"""
    from pages.data_overview import show_trend_analysis_page
    show_trend_analysis_page()

def show_user_portrait():
    """User portrait page"""
    from pages.data_overview import show_user_portrait_page
    show_user_portrait_page()

def show_heatmap():
    """Activity heatmap page"""
    from pages.behavior_analysis import show_heatmap_page
    show_heatmap_page()

def show_funnel():
    """Conversion funnel page"""
    from pages.behavior_analysis import show_funnel_page
    show_funnel_page()

def show_retention():
    """Retention analysis page"""
    from pages.behavior_analysis import show_retention_page
    show_retention_page()

def show_behavior_path():
    """Behavior path page"""
    from pages.behavior_analysis import show_behavior_path_page
    show_behavior_path_page()

def show_clustering():
    """User clustering page"""
    from pages.user_profiling import show_clustering_page
    show_clustering_page()

def show_lifecycle():
    """Lifecycle page"""
    from pages.user_profiling import show_lifecycle_page
    show_lifecycle_page()

def show_purchase_intent():
    """Purchase intent prediction page"""
    from pages.prediction_models import show_purchase_intent_page
    show_purchase_intent_page()

def show_sales_forecast():
    """Sales forecast page"""
    from pages.prediction_models import show_sales_forecast_page
    show_sales_forecast_page()

def show_realtime_dashboard():
    """Real-time dashboard page"""
    from pages.realtime_dashboard import show_realtime_dashboard
    show_realtime_dashboard()

def show_anomaly_detection():
    """Anomaly detection page"""
    from pages.anomaly_detection import show_anomaly_detection_page
    show_anomaly_detection_page()

def show_ai_chat():
    """AI chat page"""
    from pages.ai_assistant import show_ai_chat_page
    show_ai_chat_page()

def show_report_generation():
    """Report generation page"""
    from pages.ai_assistant import show_report_page
    show_report_page()

def show_pdf_export():
    """PDF export page"""
    from pages.pdf_export import show_pdf_export_page
    show_pdf_export_page()

def show_user_management():
    """User management page"""
    from pages.system_management import show_user_management_page
    show_user_management_page()

def show_system_logs():
    """System logs page"""
    from pages.system_management import show_system_logs_page
    show_system_logs_page()

def show_performance_monitor():
    """Performance monitor page"""
    from utils.performance import show_performance_dashboard
    show_performance_dashboard()

# 数据集成页面路由
def show_csv_import():
    """CSV文件导入页面"""
    from pages.data_integration import show_csv_connector
    show_csv_connector()

def show_excel_import():
    """Excel文件导入页面"""
    from pages.data_integration import show_excel_connector
    show_excel_connector()

def show_api_import():
    """API接口导入页面"""
    from pages.data_integration import show_api_connector
    show_api_connector()

if __name__ == "__main__":
    main()
