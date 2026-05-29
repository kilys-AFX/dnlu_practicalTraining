"""
AI助手模块 - MiMo集成 / 智能问答 / 报告生成
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime

from data.database import execute_query
from config.settings import MIMO_CONFIG


def init_mimo_client():
    """初始化MiMo API客户端"""
    if not MIMO_CONFIG["api_key"] or not MIMO_CONFIG["base_url"]:
        st.warning("⚠️ 请在 `config/settings.py` 中配置 MiMo API Key 和 base_url")
        return None
    
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=MIMO_CONFIG["api_key"],
            base_url=MIMO_CONFIG["base_url"]
        )
        return client
    except Exception as e:
        st.error(f"❌ MiMo客户端初始化失败: {e}")
        return None


def query_mimo(client, question, context=""):
    """
    调用MiMo API进行问答
    """
    try:
        messages = [
            {"role": "system", "content": """你是一名专业的零售数据分析助手。
            请根据提供的数据上下文回答用户问题。
            回答要简洁、专业，并提供可操作的建议。"""},
            {"role": "user", "content": f"上下文:\n{context}\n\n问题: {question}"}
        ]
        
        response = client.chat.completions.create(
            model=MIMO_CONFIG["model"],
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ API调用失败: {str(e)}"


def show_ai_chat_page():
    """AI智能问答页面"""
    st.markdown("## 🤖 AI智能问答")
    
    # 初始化聊天历史
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    # 侧边栏：快速问题
    with st.sidebar:
        st.markdown("### 💡 快速问题")
        
        quick_questions = [
            "分析用户购买行为特征",
            "哪个年龄段消费最高？",
            "如何提高用户复购率？",
            "流失用户有什么特征？",
            "商品销售趋势如何？"
        ]
        
        for q in quick_questions:
            if st.button(q, use_container_width=True, key=f"quick_{q}"):
                st.session_state["current_question"] = q
        
        st.markdown("---")
        
        if st.button("🗑️ 清除聊天历史", use_container_width=True):
            st.session_state["chat_history"] = []
            st.rerun()
    
    # 显示对话历史
    for chat in st.session_state["chat_history"]:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])
    
    # 用户输入
    question = st.chat_input("请输入您的问题...")
    
    # 如果有快速问题，使用快速问题
    if "current_question" in st.session_state:
        question = st.session_state["current_question"]
        del st.session_state["current_question"]
    
    if question:
        # 显示用户问题
        with st.chat_message("user"):
            st.write(question)
        
        # 添加到历史
        st.session_state["chat_history"].append({
            "role": "user",
            "content": question
        })
        
        # 获取数据分析上下文
        with st.spinner("🤔 AI正在思考..."):
            # 准备数据上下文
            context = prepare_data_context(question)
            
            # 调用MiMo
            client = init_mimo_client()
            if client:
                answer = query_mimo(client, question, context)
            else:
                # 模拟回答（用于演示）
                answer = generate_mock_answer(question)
            
            # 显示回答
            with st.chat_message("assistant"):
                st.write(answer)
            
            # 添加到历史
            st.session_state["chat_history"].append({
                "role": "assistant",
                "content": answer
            })


def prepare_data_context(question):
    """根据问题准备数据上下文"""
    context = ""
    
    # 基础统计
    try:
        total_users = execute_query("SELECT COUNT(*) as count FROM users").iloc[0]["count"]
        total_orders = execute_query("SELECT COUNT(*) as count FROM orders").iloc[0]["count"]
        total_gmv = execute_query("SELECT SUM(total_amount) as sum FROM orders WHERE status != 'Cancelled'").iloc[0]["sum"] or 0
        
        context += f"""
        基础数据:
        - 总用户数: {total_users}
        - 总订单数: {total_orders}
        - 总GMV: ¥{total_gmv:,.2f}
        """
    except:
        pass
    
    # 根据问题关键词添加更多上下文
    if "年龄" in question or "年龄段" in question:
        try:
            age_data = execute_query("""
            SELECT 
                CASE 
                    WHEN age < 20 THEN '20岁以下'
                    WHEN age BETWEEN 20 AND 30 THEN '20-30岁'
                    WHEN age BETWEEN 31 AND 40 THEN '31-40岁'
                    WHEN age BETWEEN 41 AND 50 THEN '41-50岁'
                    ELSE '50岁以上'
                END as age_group,
                COUNT(*) as count,
                AVG(uv.avg_amount) as avg_spent
            FROM users u
            LEFT JOIN (
                SELECT user_id, AVG(total_amount) as avg_amount
                FROM orders
                WHERE status != 'Cancelled'
                GROUP BY user_id
            ) uv ON u.user_id = uv.user_id
            GROUP BY age_group
            """)
            context += f"\n年龄分布数据:\n{age_data.to_string()}"
        except:
            pass
    
    return context


def generate_mock_answer(question):
    """生成模拟回答（用于演示）"""
    mock_answers = {
        "分析用户购买行为特征": """
        根据数据分析，用户购买行为特征如下：
        
        1. **购买时间**: 最活跃时段为晚8-10点，周末购买率比工作日高30%
        2. **购买频率**: 平均每月2.3次购买，复购率45%
        3. **客单价**: 平均客单价¥186，高价值用户（高RFM得分）可达¥500+
        4. **品类偏好**: 电子产品和服装是热销品类，占总销售额60%
        
        **建议**:
        - 在晚8-10点加大促销力度
        - 针对高价值用户推出会员专属优惠
        - 优化推荐算法，提升电子产品和服装的推荐精准度
        """,
        
        "哪个年龄段消费最高？": """
        根据数据分析，**31-40岁**年龄段消费最高：
        
        - 平均客单价: ¥235
        - 月均购买频次: 3.2次
        - 消费占比: 38%
        
        其次是**20-30岁**年龄段：
        - 平均客单价: ¥168
        - 月均购买频次: 2.8次
        - 消费占比: 32%
        
        **建议**: 针对31-40岁群体推出高品质、高价格商品；针对20-30岁群体推出性价比高的商品。
        """,
        
        "如何提高用户复购率？": """
        提高用户复购率的策略：
        
        1. **个性化推荐**: 根据用户购买历史推荐相关商品（预计提升复购率15%）
        2. **会员体系**: 推出积分、等级、专属优惠等会员权益（预计提升复购率20%）
        3. **精准营销**: 对即将流失的用户发送召回优惠券（预计提升复购率10%）
        4. **优质服务**: 提升物流速度、售后服务等（预计提升复购率12%）
        
        **优先级**: 建议先实施会员体系和精准营销，成本较低且效果显著。
        """
    }
    
    for key, answer in mock_answers.items():
        if key in question:
            return answer
    
    return f"""
    您的问题: {question}
    
    根据当前数据分析，我建议：
    
    1. 关注用户生命周期管理，尤其是流失预测
    2. 优化购买转化漏斗，提升加购→下单转化率
    3. 使用RFM模型识别高价值客户，进行差异化运营
    
    （注：这是模拟回答。配置MiMo API可获得更准确分析）
    """


def show_report_page():
    """AI报告生成页面"""
    st.markdown("## 📝 AI智能报告生成")
    
    st.markdown("根据您的数据，AI将自动生成完整的分析报告。")
    
    # 报告选项
    st.markdown("### ⚙️ 报告设置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "报告类型",
            ["综合分析", "用户行为分析", "销售趋势报告", "用户画像报告"]
        )
    
    with col2:
        report_format = st.selectbox(
            "导出格式",
            ["PDF", "Excel", "Word"]
        )
    
    # 生成报告
    if st.button("🚀 生成报告", type="primary", use_container_width=True):
        with st.spinner("正在生成报告..."):
            # 收集数据
            report_data = generate_report_data(report_type)
            
            # 调用AI生成分析报告
            client = init_mimo_client()
            
            if client:
                prompt = f"""
                请根据以下数据生成一份{report_type}，要求：
                1. 结构清晰，包括摘要、数据分析、洞察、建议
                2. 使用中文撰写
                3. 准确引用数据
                4. 提供可操作的建议
                
                数据：
                {report_data}
                """
                
                ai_report = query_mimo(client, prompt)
            else:
                # 模拟报告（用于演示）
                ai_report = generate_mock_report(report_type, report_data)
            
            # 显示报告
            st.markdown("### 📊 分析报告")
            st.markdown(ai_report)
            
            # 下载报告
            if report_format == "PDF":
                st.info("💡 PDF导出功能将在下个版本实现")
            elif report_format == "Excel":
                # 导出到Excel
                output = export_to_excel(report_data)
                st.download_button(
                    label="📥 下载Excel报告",
                    data=output,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            elif report_format == "Word":
                st.info("💡 Word导出功能将在下个版本实现")


def generate_report_data(report_type):
    """生成报告数据"""
    data = {}
    
    # 基础指标
    data["total_users"] = execute_query("SELECT COUNT(*) as count FROM users").iloc[0]["count"]
    data["total_orders"] = execute_query("SELECT COUNT(*) as count FROM orders").iloc[0]["count"]
    data["total_gmv"] = execute_query("SELECT SUM(total_amount) as sum FROM orders WHERE status != 'Cancelled'").iloc[0]["sum"] or 0
    
    # 根据报告类型添加更多数据
    if "用户" in report_type or "综合" in report_type:
        data["user_gender"] = execute_query("SELECT gender, COUNT(*) as count FROM users GROUP BY gender").to_dict("records")
        data["user_age"] = execute_query("""
        SELECT 
            CASE 
                WHEN age < 20 THEN '20岁以下'
                WHEN age BETWEEN 20 AND 30 THEN '20-30岁'
                WHEN age BETWEEN 31 AND 40 THEN '31-40岁'
                WHEN age BETWEEN 41 AND 50 THEN '41-50岁'
                ELSE '50岁以上'
            END as age_group,
            COUNT(*) as count
        FROM users
        GROUP BY age_group
        """).to_dict("records")
    
    if "销售" in report_type or "综合" in report_type:
        data["daily_sales"] = execute_query("""
        SELECT DATE(order_date) as date, SUM(total_amount) as gmv
        FROM orders
        WHERE status != 'Cancelled'
        GROUP BY DATE(order_date)
        ORDER BY date
        LIMIT 30
        """).to_dict("records")
    
    return data


def generate_mock_report(report_type, data):
    """生成模拟报告（用于演示）"""
    report = f"""
    # {report_type}
    
    **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    ---
    
    ## 📊 1. 数据概览
    
    - **总用户数**: {data.get('total_users', 0):,}
    - **总订单数**: {data.get('total_orders', 0):,}
    - **总GMV**: ¥{data.get('total_gmv', 0):,.2f}
    
    ---
    
    ## 📈 2. 数据分析
    
    ### 1. 用户分析
    
    根据RFM模型分析，用户分群如下：
    
    - **高价值客户**: ~15%，贡献45%的GMV
    - **忠诚客户**: ~25%，复购率高达60%
    - **新客户**: ~30%，需要培育
    - **流失风险客户**: ~20%，需要召回
    - **已流失客户**: ~10%，召回难度大
    
    ### 2. 行为分析
    
    - **活跃时段**: 晚8-10点是最活跃时段
    - **转化漏斗**: 浏览→加购转化率25%，加购→下单转化率60%，下单→支付转化率85%
    - **留存率**: 次日留存40%，7日留存25%，30日留存15%
    
    ---
    
    ## 💡 3. 洞察
    
    1. **高价值客户是核心**: 虽然只占15%，但贡献了近一半的GMV，需要重点维护
    2. **新客户转化有提升空间**: 浏览→加购转化率只有25%，可优化商品详情页
    3. **流失风险客户需要及时干预**: 20%的客户有流失风险，建议发送召回优惠券
    
    ---
    
    ## 🎯 4. 行动建议
    
    1. **短期（1个月内）**:
       - 针对高价值客户推出会员专属活动
       - 优化商品详情页，提升加购转化率
       - 对流失风险客户发送召回优惠券
    
    2. **中期（3个月内）**:
       - 建立用户生命周期管理体系
       - 完善个性化推荐算法
       - 推出积分会员体系
    
    3. **长期（6个月内）**:
       - 建立完善的用户画像体系
       - 实现精准营销自动化
       - 提升用户LTV（生命周期价值）
    
    ---
    
    **报告生成完成**
    
    （注：这是模拟报告。配置MiMo API可获得更准确分析）
    """
    
    return report


def export_to_excel(data):
    """导出数据到Excel"""
    import io
    from openpyxl import Workbook
    
    wb = Workbook()
    ws = wb.active
    ws.title = "报告数据"
    
    # 写入数据
    ws.append(["指标", "数值"])
    for key, value in data.items():
        if isinstance(value, (int, float)):
            ws.append([key, value])
        elif isinstance(value, list):
            ws.append([key, len(value)])
    
    # 保存到内存
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    return output


if __name__ == "__main__":
    show_ai_chat_page()
