# 智能零售用户行为分析系统

🛒 基于 Streamlit + PyTorch + MiMo API 的智能零售数据分析平台

## 📋 项目概述

本项目是一个面向零售企业的用户行为分析系统，提供从数据管理、行为分析到 AI 智能洞察的全流程分析能力。

### 核心功能

- 📊 **数据管理**：上传、预览、清洗数据
- 📈 **数据概览**：关键指标、趋势分析、用户画像
- 🔍 **行为分析**：活跃热力图、转化漏斗、留存分析、行为路径
- 👤 **用户画像**：RFM 分析、K-Means 聚类、生命周期管理
- 🤖 **AI 助手**：智能问答、自动报告生成（基于 MiMo API）

## 🚀 快速开始

### 1. 安装依赖

```bash
cd d:\codebuddy\education\retail_analytics
pip install -r requirements.txt
```

### 2. 配置 MiMo API（可选）

编辑 `config/settings.py`，填写您的 MiMo API 信息：

```python
MIMO_CONFIG = {
    "api_key": "your_api_key_here",
    "base_url": "your_base_url_here",
    "model": "your_model_name_here",
}
```

如果不配置，系统将使用模拟回答功能。

### 3. 运行系统

```bash
streamlit run app.py
```

系统将自动在浏览器中打开，默认地址：http://localhost:8501

### 4. 生成模拟数据

在左侧边栏点击「🔄 生成模拟数据」按钮，系统将自动生成测试数据。

## 📂 项目结构

```
retail_analytics/
├── app.py                 # 主入口
├── config/                # 配置文件
│   └── settings.py        # 配置项
├── data/                  # 数据层
│   ├── __init__.py
│   ├── database.py        # 数据库初始化
│   └── data_generator.py  # 模拟数据生成
├── models/                # PyTorch 模型（待实现）
├── pages/                 # 页面模块
│   ├── data_management.py # 数据管理
│   ├── data_overview.py   # 数据概览
│   ├── behavior_analysis.py # 行为分析
│   ├── user_profiling.py  # 用户画像
│   └── ai_assistant.py    # AI 助手
├── utils/                 # 工具函数
│   └── data_processor.py # 数据处理
├── assets/                # 静态资源
├── requirements.txt       # 依赖包
└── README.md              # 说明文档
```

## 📊 使用指南

### 数据管理

1. **上传数据**：支持 CSV、Excel 格式，可上传到用户表、订单表、商品表、行为日志表
2. **生成模拟数据**：一键生成 1000 用户 + 200 商品 + 5000 订单 + 50000 行为记录
3. **数据清洗**：去重、填充缺失值、异常值处理

### 数据概览

- **关键指标**：总用户、总订单、GMV、转化率
- **趋势分析**：日活跃趋势、用户增长趋势
- **用户画像**：性别分布、年龄分布、城市分布

### 行为分析

- **活跃热力图**：按小时×星期的用户活跃热力图
- **转化漏斗**：浏览→加购→下单→支付转化率
- **留存分析**：次日/7日/30日留存曲线
- **行为路径**：桑基图展示用户行为路径

### 用户画像

- **RFM 分析**：Recency/Frequency/Monetary 三维用户价值分群
- **K-Means 聚类**：基于用户特征的自动分群
- **生命周期**：新客/活跃/流失预警/流失客户识别

### AI 助手

- **智能问答**：用中文询问数据问题，AI 自动回答
- **报告生成**：一键生成综合分析报告（支持 Excel 导出）

## 🔧 技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| 前端 | Streamlit + Ant Design | UI 框架 |
| 数据处理 | Pandas + NumPy | 数据清洗、分析 |
| 可视化 | Plotly | 交互式图表 |
| 机器学习 | Scikit-learn | RFM、聚类、留存分析 |
| 深度学习 | PyTorch（待实现） | 购买预测、销量预测 |
| 数据库 | SQLite | 轻量数据存储 |
| AI 大模型 | MiMo API（小米） | 智能问答、报告生成 |

## 📝 开发计划

### MVP 第一期（当前版本）

- ✅ 数据管理（上传/预览/清洗）
- ✅ 数据概览（指标/趋势/画像）
- ✅ 行为分析（热力图/漏斗/留存）
- ✅ 用户画像（RFM/聚类/生命周期）
- ✅ AI 助手（问答/报告）

### 第二期（待开发）

- ⬜ PyTorch 预测模型（购买意向、销量预测）
- ⬜ 实时监控大屏
- ⬜ 异常预警播报
- ⬜ PDF 报告导出

### 第三期（待开发）

- ⬜ 主题切换（亮色/暗色）
- ⬜ 中英文切换
- ⬜ 部署到服务器

## ❓ 常见问题

### 1. 如何获取 MiMo API Key？

访问小米 AI 开放平台（具体地址待用户确认），申请 API Key。

### 2. 数据表结构是什么？

系统包含 5 张表：
- `users`：用户表（user_id, gender, age, city, register_date, last_login）
- `products`：商品表（product_id, product_name, category, price, stock）
- `orders`：订单表（order_id, user_id, order_date, total_amount, status）
- `order_items`：订单明细表（item_id, order_id, product_id, quantity, price）
- `user_behavior`：行为日志表（behavior_id, user_id, product_id, behavior_type, behavior_time, duration, device, channel）

### 3. 如何自定义数据分析？

可以在「AI 助手 - 智能问答」中用中文提问，AI 会根据数据自动分析。

## 📧 联系方式

- 开发者：AI 专业研究生
- 开发 IDE：CodeBuddy
- 版本：1.0.0 MVP

## 📄 许可证

本项目仅供学习和研究使用。
