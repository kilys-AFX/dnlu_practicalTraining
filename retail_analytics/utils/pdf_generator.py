"""
PDF 报告生成器
"""
import os
from pathlib import Path
from datetime import datetime
import pandas as pd

# 检查是否有 WeasyPrint（优先使用）
try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

# 检查是否有 reportlab（备用方案）
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_pdf_report(data_dict, output_path=None):
    """
    生成 PDF 分析报告
    参数：
        data_dict: 数据字典，包含各项分析数据
        output_path: 输出文件路径（可选，默认为项目根目录下的 reports/）
    返回：
        output_path: 生成的 PDF 文件路径
    """
    if not WEASYPRINT_AVAILABLE and not REPORTLAB_AVAILABLE:
        raise ImportError("需要安装 weasyprint 或 reportlab 才能生成 PDF")
    
    # 确定输出路径
    if output_path is None:
        reports_dir = Path("reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        output_path = reports_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 优先使用 WeasyPrint（HTML → PDF，更适合带图表的报告）
    if WEASYPRINT_AVAILABLE:
        return _generate_pdf_weasyprint(data_dict, output_path)
    else:
        return _generate_pdf_reportlab(data_dict, output_path)


def _generate_pdf_weasyprint(data_dict, output_path):
    """使用 WeasyPrint 生成 PDF（HTML → PDF）"""
    from weasyprint import HTML
    from jinja2 import Template
    
    # HTML 模板
    html_template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>智能零售用户行为分析报告</title>
        <style>
            body { font-family: "SimHei", "Microsoft YaHei", sans-serif; margin: 2cm; }
            h1 { color: #1E88E5; border-bottom: 2px solid #1E88E5; padding-bottom: 10px; }
            h2 { color: #333; margin-top: 20px; }
            table { width: 100%; border-collapse: collapse; margin: 15px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #1E88E5; color: white; }
            .metric { display: inline-block; width: 23%; margin: 10px 1%; padding: 15px; background: #f5f5f5; border-radius: 5px; }
            .metric-value { font-size: 24px; font-weight: bold; color: #1E88E5; }
            .metric-label { font-size: 14px; color: #666; }
            .footer { margin-top: 50px; text-align: center; color: #999; font-size: 12px; }
        </style>
    </head>
    <body>
        <h1>🛒 智能零售用户行为分析报告</h1>
        <p>生成时间：{{ generate_time }}</p>
        
        <h2>一、数据概览</h2>
        <div class="metric">
            <div class="metric-value">{{ total_users }}</div>
            <div class="metric-label">总用户数</div>
        </div>
        <div class="metric">
            <div class="metric-value">{{ total_orders }}</div>
            <div class="metric-label">总订单数</div>
        </div>
        <div class="metric">
            <div class="metric-value">¥{{ total_gmv }}</div>
            <div class="metric-label">GMV</div>
        </div>
        <div class="metric">
            <div class="metric-value">{{ conversion_rate }}%</div>
            <div class="metric-label">转化率</div>
        </div>
        
        <h2>二、用户画像</h2>
        {% if user_gender %}
        <table>
            <tr><th>性别</th><th>用户数</th></tr>
            {% for item in user_gender %}
            <tr><td>{{ item.gender }}</td><td>{{ item.count }}</td></tr>
            {% endfor %}
        </table>
        {% endif %}
        
        <h2>三、RFM 分析</h2>
        {% if rfm_segments %}
        <table>
            <tr><th>用户分群</th><th>用户数</th><th>占比</th></tr>
            {% for segment, count in rfm_segments.items() %}
            <tr><td>{{ segment }}</td><td>{{ count }}</td><td>{{ (count / total_users * 100) | round(1) }}%</td></tr>
            {% endfor %}
        </table>
        {% endif %}
        
        <h2>四、行为分析</h2>
        {% if behavior_funnel %}
        <table>
            <tr><th>行为阶段</th><th>用户数</th><th>转化率</th></tr>
            {% for item in behavior_funnel %}
            <tr><td>{{ item.step }}</td><td>{{ item.users }}</td><td>{{ item.conversion_rate | round(1) }}%</td></tr>
            {% endfor %}
        </table>
        {% endif %}
        
        <h2>五、数据洞察</h2>
        <ul>
            <li>高价值客户占比 {{ high_value_pct }}%，贡献了 {{ high_value_gmv_pct }}% 的 GMV</li>
            <li>浏览到加购转化率 {{ browse_to_cart_rate }}%，有提升空间</li>
            <li>用户最活跃时段：{{ peak_hour }}</li>
        </ul>
        
        <h2>六、行动建议</h2>
        <ol>
            <li>针对高价值客户推出会员专属活动</li>
            <li>优化商品详情页，提升加购转化率</li>
            <li>对流失风险客户发送召回优惠券</li>
            <li>在用户活跃时段加大推广力度</li>
        </ol>
        
        <div class="footer">
            <p>本报告由「智能零售用户行为分析系统」自动生成</p>
            <p>如需详细数据，请联系数据分析团队</p>
        </div>
    </body>
    </html>
    """)
    
    # 准备模板数据
    template_data = {
        "generate_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_users": data_dict.get("total_users", 0),
        "total_orders": data_dict.get("total_orders", 0),
        "total_gmv": f"{data_dict.get('total_gmv', 0):.2f}",
        "conversion_rate": round(data_dict.get("conversion_rate", 0), 2),
        "user_gender": data_dict.get("user_gender", []),
        "rfm_segments": data_dict.get("rfm_segments", {}),
        "behavior_funnel": data_dict.get("behavior_funnel", []),
        "high_value_pct": data_dict.get("high_value_pct", 0),
        "high_value_gmv_pct": data_dict.get("high_value_gmv_pct", 0),
        "browse_to_cart_rate": data_dict.get("browse_to_cart_rate", 0),
        "peak_hour": data_dict.get("peak_hour", "N/A"),
    }
    
    # 渲染 HTML
    html_content = html_template.render(**template_data)
    
    # 生成 PDF
    HTML(string=html_content).write_pdf(str(output_path))
    
    return output_path


def _generate_pdf_reportlab(data_dict, output_path):
    """使用 ReportLab 生成 PDF（纯 Python 方案）"""
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    
    # 创建 PDF 文档
    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # 标题
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor("#1E88E5"),
        spaceAfter=30,
    )
    story.append(Paragraph("智能零售用户行为分析报告", title_style))
    story.append(Spacer(1, 0.5*cm))
    
    # 生成时间
    story.append(Paragraph(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 1*cm))
    
    # 数据概览
    story.append(Paragraph("一、数据概览", styles["Heading2"]))
    
    overview_data = [
        ["指标", "数值"],
        ["总用户数", str(data_dict.get("total_users", 0))],
        ["总订单数", str(data_dict.get("total_orders", 0))],
        ["GMV", f"¥{data_dict.get('total_gmv', 0):.2f}"],
        ["转化率", f"{data_dict.get('conversion_rate', 0):.2f}%"],
    ]
    
    overview_table = Table(overview_data, colWidths=[6*cm, 6*cm])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E88E5")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 1*cm))
    
    # RFM 分析
    if "rfm_segments" in data_dict:
        story.append(Paragraph("二、RFM 分析", styles["Heading2"]))
        
        rfm_data = [["用户分群", "用户数", "占比"]]
        total_users = data_dict.get("total_users", 1)
        
        for segment, count in data_dict["rfm_segments"].items():
            pct = (count / total_users * 100) if total_users > 0 else 0
            rfm_data.append([segment, str(count), f"{pct:.1f}%"])
        
        rfm_table = Table(rfm_data, colWidths=[4*cm, 4*cm, 4*cm])
        rfm_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FF6F00")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(rfm_table)
        story.append(Spacer(1, 1*cm))
    
    # 行为分析
    if "behavior_funnel" in data_dict:
        story.append(Paragraph("三、行为分析（转化漏斗）", styles["Heading2"]))
        
        funnel_data = [["行为阶段", "用户数", "转化率"]]
        for item in data_dict["behavior_funnel"]:
            funnel_data.append([
                item["step"],
                str(item["users"]),
                f"{item.get('conversion_rate', 0):.1f}%"
            ])
        
        funnel_table = Table(funnel_data, colWidths=[4*cm, 4*cm, 4*cm])
        funnel_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#43A047")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(funnel_table)
        story.append(Spacer(1, 1*cm))
    
    # 行动建议
    story.append(Paragraph("四、行动建议", styles["Heading2"]))
    
    suggestions = [
        "1. 针对高价值客户推出会员专属活动",
        "2. 优化商品详情页，提升加购转化率",
        "3. 对流失风险客户发送召回优惠券",
        "4. 在用户活跃时段加大推广力度",
    ]
    
    for suggestion in suggestions:
        story.append(Paragraph(suggestion, styles["Normal"]))
        story.append(Spacer(1, 0.3*cm))
    
    # 生成 PDF
    doc.build(story)
    
    return output_path


def get_report_data():
    """
    从数据库获取报告所需数据
    """
    from data.database import execute_query
    
    data = {}
    
    # 基础指标
    data["total_users"] = execute_query("SELECT COUNT(DISTINCT user_id) as count FROM users").iloc[0]["count"]
    data["total_orders"] = execute_query("SELECT COUNT(DISTINCT order_id) as count FROM orders").iloc[0]["count"]
    data["total_gmv"] = execute_query("SELECT SUM(total_amount) as sum FROM orders WHERE status != '已取消'").iloc[0]["sum"] or 0
    
    paid_users = execute_query("SELECT COUNT(DISTINCT user_id) as count FROM orders WHERE status != '已取消'").iloc[0]["count"]
    data["conversion_rate"] = (paid_users / data["total_users"] * 100) if data["total_users"] > 0 else 0
    
    # 用户画像
    data["user_gender"] = execute_query("SELECT gender, COUNT(*) as count FROM users GROUP BY gender").to_dict("records")
    
    # RFM 分析
    orders = execute_query("SELECT user_id, order_date, total_amount FROM orders WHERE status != '已取消'")
    if not orders.empty:
        from utils.data_processor import calculate_rfm
        rfm = calculate_rfm(orders)
        data["rfm_segments"] = rfm["Segment"].value_counts().to_dict()
    
    # 行为分析
    funnel = execute_query("""
    SELECT behavior_type, COUNT(DISTINCT user_id) as users
    FROM user_behavior
    WHERE behavior_type IN ('浏览', '加购', '下单', '支付')
    GROUP BY behavior_type
    ORDER BY CASE behavior_type
        WHEN '浏览' THEN 1
        WHEN '加购' THEN 2
        WHEN '下单' THEN 3
        WHEN '支付' THEN 4
    END
    """)
    
    if not funnel.empty:
        funnel["conversion_rate"] = funnel["users"] / funnel["users"].iloc[0] * 100
        data["behavior_funnel"] = funnel.to_dict("records")
    
    # 数据洞察
    rfm_segments = data.get("rfm_segments", {})
    high_value_count = rfm_segments.get("高价值客户", 0)
    data["high_value_pct"] = (high_value_count / data["total_users"] * 100) if data["total_users"] > 0 else 0
    data["browse_to_cart_rate"] = 20.5  # 模拟数据
    data["peak_hour"] = "20:00-22:00"
    
    return data


if __name__ == "__main__":
    # 测试 PDF 生成
    print("正在生成测试报告...")
    
    try:
        # 获取报告数据
        report_data = get_report_data()
        
        # 生成 PDF
        output_path = generate_pdf_report(report_data)
        
        print(f"✅ 报告已生成：{output_path}")
        
    except Exception as e:
        print(f"❌ 报告生成失败：{e}")
        print("\n请安装依赖：")
        print("  pip install weasyprint")
        print("  或")
        print("  pip install reportlab")
