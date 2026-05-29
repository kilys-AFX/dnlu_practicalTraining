"""
智能零售用户行为分析系统 - 主入口 (柔和现代风)
"""
import streamlit as st
import streamlit_antd_components as sac
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from utils.auth import init_auth_db, authenticate_user, get_user_by_id, update_last_login, check_permission, create_user
from config.settings import APP_CONFIG

st.set_page_config(
    page_title=APP_CONFIG["title"],
    page_icon=APP_CONFIG["icon"],
    layout=APP_CONFIG["layout"],
    initial_sidebar_state=APP_CONFIG["initial_sidebar_state"]
)

# ============================================
# CSS
# ============================================
def load_css():
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    # 隐藏 Streamlit 默认的英文页面导航和顶部空白
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    .stAppToolbar { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ============================================
# SIDEBAR
# ============================================
def sidebar_navigation():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0 8px;">
            <div style="font-size:38px;">🛒</div>
            <div style="font-size:1.1rem; font-weight:700; color:#4C1D95; margin-top:6px;">零售分析平台</div>
            <div style="font-size:0.7rem; color:#8B5CF6; margin-top:2px; font-weight:500;">v3.0.0 · Soft Modern</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        if st.session_state.user:
            user = st.session_state.user
            role_map = {"admin": "管理员", "manager": "运营经理", "user": "普通用户"}
            role_icon = {"admin": "👑", "manager": "⭐", "user": "👤"}

            st.markdown(f"""
            <div class="sidebar-user-card">
                <div class="avatar">{role_icon.get(user['role'], '👤')}</div>
                <h3>{user['username']}</h3>
                <p>{role_map.get(user['role'], user['role'])}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚪 退出登录", key="logout_btn", use_container_width=True):
                st.session_state.user = None
                st.rerun()

        st.markdown("---")

        menu_items = [
            sac.MenuItem("数据管理", icon="database", children=[
                sac.MenuItem("数据上传", icon="upload"),
                sac.MenuItem("数据预览", icon="eye"),
                sac.MenuItem("数据清洗", icon="sparkles"),
            ]),
            sac.MenuItem("数据概览", icon="bar-chart", children=[
                sac.MenuItem("核心指标", icon="dashboard"),
                sac.MenuItem("趋势分析", icon="trending-up"),
                sac.MenuItem("用户画像概览", icon="pie-chart"),
            ]),
            sac.MenuItem("行为分析", icon="activity", children=[
                sac.MenuItem("活跃热力图", icon="heatmap"),
                sac.MenuItem("转化漏斗", icon="filter"),
                sac.MenuItem("留存分析", icon="repeat"),
                sac.MenuItem("行为路径", icon="git-branch"),
            ]),
            sac.MenuItem("用户画像", icon="users", children=[
                sac.MenuItem("用户聚类", icon="cluster"),
                sac.MenuItem("生命周期", icon="clock"),
            ]),
        ]

        if check_permission(st.session_state.user['role'], 'user'):
            menu_items.append(sac.MenuItem("预测模型", icon="brain", children=[
                sac.MenuItem("购买意向", icon="target"),
                sac.MenuItem("销售预测", icon="trending-up"),
            ]))
            menu_items.append(sac.MenuItem("实时监控", icon="monitor", children=[
                sac.MenuItem("数据大屏", icon="tv"),
                sac.MenuItem("异常检测", icon="alert-triangle"),
            ]))

        if check_permission(st.session_state.user['role'], 'manager'):
            menu_items.append(sac.MenuItem("AI助手", icon="robot", children=[
                sac.MenuItem("智能问答", icon="message-circle"),
                sac.MenuItem("报告生成", icon="file-text"),
                sac.MenuItem("PDF导出", icon="file"),
            ]))
            menu_items.append(sac.MenuItem("数据集成", icon="database-add", children=[
                sac.MenuItem("CSV文件", icon="file-text"),
                sac.MenuItem("Excel文件", icon="file-excel"),
                sac.MenuItem("API接口", icon="cloud"),
            ]))

        if check_permission(st.session_state.user['role'], 'admin'):
            menu_items.append(sac.MenuItem("系统管理", icon="settings", children=[
                sac.MenuItem("用户管理", icon="people"),
                sac.MenuItem("系统日志", icon="journal-text"),
                sac.MenuItem("性能监控", icon="speedometer"),
            ]))

        selected = sac.menu(items=menu_items, open_all=True, return_index=False)

        st.markdown("---")

        if check_permission(st.session_state.user['role'], 'manager'):
            if st.button("🔄 生成模拟数据", use_container_width=True):
                with st.spinner("正在生成模拟数据..."):
                    from data.data_generator import generate_all_data
                    generate_all_data()
                    st.success("数据生成成功！")
                    st.rerun()

        st.markdown("""
        <div style="text-align:center; padding:20px 0 8px;">
            <div style="font-size:0.7rem; color:#A78BFA;">AI研究生 · CodeBuddy</div>
            <div style="font-size:0.6rem; color:#C4B5FD; margin-top:3px;">仅供学习研究使用</div>
        </div>
        """, unsafe_allow_html=True)

    return selected

# ============================================
# LOGIN
# ============================================
def check_login():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if st.session_state.user is None:
        show_login_page()
        return False
    return True

def show_login_page():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stApp { background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 30%, #E0F2FE 70%, #ECFDF5 100%) !important; }
    .main .block-container { padding-top: 3rem !important; }
    </style>
    """, unsafe_allow_html=True)

    # 判断是否在注册页面
    if st.session_state.get("show_register", False):
        show_register_page()
        return

    _, col, _ = st.columns([1, 1.1, 1])

    with col:
        st.markdown("""
        <div class="login-brand">
            <span class="brand-icon">🛒</span>
            <div class="brand-name">零售数据分析平台</div>
            <div class="brand-sub">AI 驱动的智能零售解决方案</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-card-outer">', unsafe_allow_html=True)
        st.markdown("### 🔐 账号登录")

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("用户名", placeholder="请输入用户名")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            submit = st.form_submit_button("登 录", type="primary", use_container_width=True)

            if submit:
                if not username or not password:
                    st.error("请输入用户名和密码")
                else:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.user = user
                        update_last_login(user['id'])
                        st.success("登录成功，正在跳转...")
                        st.rerun()
                    else:
                        st.error("用户名或密码错误")

        st.markdown('</div>', unsafe_allow_html=True)

        # 注册按钮 - 跳转到注册页面
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📝 注册新账号", use_container_width=True, type="secondary"):
            st.session_state.show_register = True
            st.rerun()

    # 底部提示
    st.markdown("""
    <div style="text-align:center; margin-top:24px; opacity:0.5;">
        <div style="font-size:0.7rem; color:#A78BFA;">仅供学习研究使用</div>
    </div>
    """, unsafe_allow_html=True)


def show_register_page():
    """独立的注册页面"""
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .main .block-container { padding-top: 3rem !important; }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])

    with col:
        st.markdown("""
        <div class="login-brand">
            <span class="brand-icon">📝</span>
            <div class="brand-name">注册新账号</div>
            <div class="brand-sub">创建您的零售分析平台账号</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-card-outer">', unsafe_allow_html=True)
        st.markdown("### 📋 填写注册信息")

        with st.form("register_form"):
            nu = st.text_input("用户名", placeholder="请输入用户名")
            ne = st.text_input("邮箱", placeholder="请输入邮箱地址")
            c1, c2 = st.columns(2)
            with c1:
                np = st.text_input("密码", type="password", placeholder="至少6位")
            with c2:
                nc = st.text_input("确认密码", type="password", placeholder="再次输入密码")
            nr = st.selectbox("角色权限", ["普通用户 (user)", "运营经理 (manager)", "管理员 (admin)"])

            submitted = st.form_submit_button("注 册", type="primary", use_container_width=True)

            if submitted:
                if not nu or not np or not ne:
                    st.error("请填写完整信息")
                elif np != nc:
                    st.error("两次密码不一致")
                elif len(np) < 6:
                    st.error("密码长度至少6位")
                else:
                    role_map = {"普通用户 (user)": "user", "运营经理 (manager)": "manager", "管理员 (admin)": "admin"}
                    role = role_map.get(nr, "user")
                    if create_user(nu, np, ne, role):
                        st.success(f"注册成功！即将跳转到登录页...")
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error("用户名已存在")

        st.markdown('</div>', unsafe_allow_html=True)

        # 返回登录按钮
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← 返回登录", use_container_width=True, type="secondary"):
            st.session_state.show_register = False
            st.rerun()

# ============================================
# HOME PAGE
# ============================================
def show_home():
    now = datetime.now()
    hour = now.hour
    greeting = "早上好" if hour < 12 else ("下午好" if hour < 18 else "晚上好")

    user = st.session_state.user

    st.markdown(f"""
    <div class="greeting-bar">
        <div class="greeting-text">
            <h1>{greeting}, {user['username']} 👋</h1>
            <p>{now.strftime('%Y年%m月%d日')} · 欢迎回到零售分析平台</p>
        </div>
        <div class="date-badge">
            <span class="dot"></span> 系统运行中
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 快速指标
    try:
        from data.database import execute_query
        total_users = execute_query("SELECT COUNT(*) as c FROM users").iloc[0]["c"]
        total_orders = execute_query("SELECT COUNT(*) as c FROM orders").iloc[0]["c"]
        total_gmv = execute_query("SELECT SUM(total_amount) as s FROM orders WHERE status!='Cancelled'").iloc[0]["s"] or 0
        active_today = execute_query("SELECT COUNT(DISTINCT user_id) as c FROM orders WHERE date(order_date)=date('now')").iloc[0]["c"]
    except:
        total_users, total_orders, total_gmv, active_today = 0, 0, 0, 0

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric-card card-purple">
            <div class="metric-header">
                <div class="metric-icon-circle">👥</div>
                <div class="metric-badge">总用户</div>
            </div>
            <div class="metric-value">{total_users:,}</div>
            <div class="metric-label">注册用户总数</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card card-green">
            <div class="metric-header">
                <div class="metric-icon-circle">📦</div>
                <div class="metric-badge">订单</div>
            </div>
            <div class="metric-value">{total_orders:,}</div>
            <div class="metric-label">累计订单总数</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card card-blue">
            <div class="metric-header">
                <div class="metric-icon-circle">💰</div>
                <div class="metric-badge">GMV</div>
            </div>
            <div class="metric-value">¥{total_gmv:,.0f}</div>
            <div class="metric-label">累计销售额</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card card-orange">
            <div class="metric-header">
                <div class="metric-icon-circle">🔥</div>
                <div class="metric-badge">今日</div>
            </div>
            <div class="metric-value">{active_today:,}</div>
            <div class="metric-label">今日活跃用户</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🚀 核心功能")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="feature-card accent-purple"><span class="card-icon">📊</span><h4>数据管理</h4><p>CSV/Excel上传<br>一键生成模拟数据<br>智能清洗引擎</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card accent-green"><span class="card-icon">🔍</span><h4>行为分析</h4><p>活跃热力图矩阵<br>购买转化漏斗<br>留存率曲线分析</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card accent-blue"><span class="card-icon">🧠</span><h4>预测模型</h4><p>购买意向预测<br>销售趋势预测<br>LSTM深度学习</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="feature-card accent-orange"><span class="card-icon">📺</span><h4>实时监控</h4><p>数据可视化大屏<br>异常检测告警<br>性能实时追踪</p></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="feature-card accent-pink"><span class="card-icon">👤</span><h4>用户画像</h4><p>RFM价值分析<br>K-Means自动聚类<br>生命周期管理</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card accent-purple"><span class="card-icon">📈</span><h4>数据概览</h4><p>核心指标总览<br>趋势分析看板<br>多维度可视化</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card accent-green"><span class="card-icon">🤖</span><h4>AI助手</h4><p>智能数据问答<br>自动报告生成<br>MiMo大模型驱动</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="feature-card accent-blue"><span class="card-icon">🔗</span><h4>数据集成</h4><p>多格式文件导入<br>API接口对接<br>数据同步管理</p></div>', unsafe_allow_html=True)

# ============================================
# ROUTING
# ============================================
def main():
    init_auth_db()
    if not check_login():
        return
    selected = sidebar_navigation()

    if selected is None or "数据上传" in str(selected):
        from pages.data_management import show_data_upload_page; show_data_upload_page()
    elif "数据预览" in str(selected):
        from pages.data_management import show_data_preview_page; show_data_preview_page()
    elif "数据清洗" in str(selected):
        from pages.data_management import show_data_clean_page; show_data_clean_page()
    elif "核心指标" in str(selected):
        from pages.data_overview import show_key_metrics_page; show_key_metrics_page()
    elif "趋势分析" in str(selected):
        from pages.data_overview import show_trend_analysis_page; show_trend_analysis_page()
    elif "用户画像概览" in str(selected):
        from pages.data_overview import show_user_portrait_page; show_user_portrait_page()
    elif "活跃热力图" in str(selected):
        from pages.behavior_analysis import show_heatmap_page; show_heatmap_page()
    elif "转化漏斗" in str(selected):
        from pages.behavior_analysis import show_funnel_page; show_funnel_page()
    elif "留存分析" in str(selected):
        from pages.behavior_analysis import show_retention_page; show_retention_page()
    elif "行为路径" in str(selected):
        from pages.behavior_analysis import show_behavior_path_page; show_behavior_path_page()
    elif "用户聚类" in str(selected):
        from pages.user_profiling import show_clustering_page; show_clustering_page()
    elif "生命周期" in str(selected):
        from pages.user_profiling import show_lifecycle_page; show_lifecycle_page()
    elif "购买意向" in str(selected):
        from pages.prediction_models import show_purchase_intent_page; show_purchase_intent_page()
    elif "销售预测" in str(selected):
        from pages.prediction_models import show_sales_forecast_page; show_sales_forecast_page()
    elif "数据大屏" in str(selected):
        from pages.realtime_dashboard import show_realtime_dashboard; show_realtime_dashboard()
    elif "异常检测" in str(selected):
        from pages.anomaly_detection import show_anomaly_detection_page; show_anomaly_detection_page()
    elif "智能问答" in str(selected):
        from pages.ai_assistant import show_ai_chat_page; show_ai_chat_page()
    elif "报告生成" in str(selected):
        from pages.ai_assistant import show_report_page; show_report_page()
    elif "PDF导出" in str(selected):
        from pages.pdf_export import show_pdf_export_page; show_pdf_export_page()
    elif "用户管理" in str(selected):
        from pages.system_management import show_user_management_page; show_user_management_page()
    elif "系统日志" in str(selected):
        from pages.system_management import show_system_logs_page; show_system_logs_page()
    elif "CSV文件" in str(selected):
        from pages.data_integration import show_csv_connector; show_csv_connector()
    elif "Excel文件" in str(selected):
        from pages.data_integration import show_excel_connector; show_excel_connector()
    elif "API接口" in str(selected):
        from pages.data_integration import show_api_connector; show_api_connector()
    elif "性能监控" in str(selected):
        from utils.performance import show_performance_dashboard; show_performance_dashboard()
    else:
        show_home()

if __name__ == "__main__":
    main()
