# 智能零售用户行为分析系统

> Intelligent Retail User Behavior Analytics System

<div align="center">

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-Educational-orange)
![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red)
![PyTorch](https://img.shields.io/badge/pytorch-2.0+-ee4c2c)

**基于 Streamlit + PyTorch + MiMo API 的全栈智能零售数据分析平台**

[功能特性](#-功能特性) · [快速开始](#-快速开始) · [系统架构](#-系统架构) · [模块详解](#-模块详解) · [技术栈](#-技术栈) · [部署指南](#-部署指南)

</div>

---

## 📋 项目概述

本项目是一套面向零售企业的**智能用户行为分析系统**，采用分层架构设计，集数据管理、行为分析、用户画像、AI 预测模型、实时监控和智能问答于一体。系统支持从数据接入到 AI 洞察的全流程闭环，帮助零售企业实现数据驱动的精细化运营。

### 🎯 项目背景

- **项目来源**：2026人工智能研究生实训项目
- **开发环境**：CodeBuddy IDE + SpecKit 规范化开发
- **当前版本**：v3.0.0

---

## ✨ 功能特性

### 🗂️ 数据管理
| 功能 | 描述 |
|------|------|
| **多源数据接入** | 支持 CSV / Excel / JSON / API / 数据库 5 种数据源导入 |
| **智能编码检测** | 自动识别 UTF-8 / GBK / GB2312 / UTF-16 等编码格式 |
| **模拟数据生成** | 一键生成 1000+ 用户、200+ 商品、5000+ 订单、50000+ 行为记录 |
| **数据清洗引擎** | 去重、缺失值填充（均值/中位数/众数）、IQR 异常值截断 |
| **数据预览统计** | 字段信息、统计摘要、数据质量报告 |

### 📊 数据概览
| 功能 | 描述 |
|------|------|
| **关键指标看板** | 总用户、总订单、GMV、转化率 4 大核心指标卡片 |
| **日活趋势分析** | 每日活跃用户数折线图 + 订单量与 GMV 双轴趋势图 |
| **用户增长追踪** | 每日新增用户趋势分析 |
| **用户画像概览** | 性别饼图、年龄分布柱状图、城市 TOP10 排行 |

### 🔍 行为分析
| 功能 | 描述 |
|------|------|
| **活跃热力图** | 按小时 × 星期的用户活跃度矩阵热力图（Plotly） |
| **转化漏斗** | 浏览 → 加购 → 下单 → 支付 四层转化漏斗，含优化建议 |
| **留存曲线** | 1日 / 3日 / 7日 / 14日 / 30日 用户留存率追踪 |
| **行为路径** | 桑基图可视化用户行为流转路径 |

### 👤 用户画像
| 功能 | 描述 |
|------|------|
| **K-Means 聚类** | 可配置聚类数（2-10）和特征选择，雷达图展示聚类中心 |
| **RFM 客户价值** | 六类客户细分（冠军客户 / 忠实客户 / 新客户 / 流失风险 / 高价值流失 / 一般客户） |
| **生命周期管理** | 潜在 → 新客 → 忠实 → 流失预警 → 流失 五阶段分类 + 运营策略 |

### 🤖 AI 预测模型
| 功能 | 描述 |
|------|------|
| **购买意向预测** | PyTorch MLP 二分类，12+ 维特征工程，含早停 + 学习率调度 |
| **销售预测** | 双 LSTM 层时序模型，自回归滚动预测未来 N 天销售额 |

### 📡 实时监控
| 功能 | 描述 |
|------|------|
| **实时数据大屏** | 5 秒自动刷新，在线用户 / 今日订单 / GMV / 转化率实时展示 |
| **异常检测播报** | Z-Score 统计方法，灵敏度可调，AI 智能诊断异常原因 |

### 🧠 AI 智能助手
| 功能 | 描述 |
|------|------|
| **智能问答** | 基于 MiMo API（OpenAI 兼容），自然语言查询数据洞察 |
| **自动报告生成** | 一键生成综合分析 / 用户行为 / 销售趋势 / 用户画像报告，支持 Excel 导出 |

### 🔐 系统管理
| 功能 | 描述 |
|------|------|
| **三级权限控制** | admin（管理员）/ manager（经理）/ user（普通用户）RBAC 角色体系 |
| **用户管理** | 创建用户、状态切换、删除用户（admin 专属） |
| **安全认证** | PBKDF2-HMAC-SHA256 密码哈希，会话状态管理 |

---

## 🚀 快速开始

### 环境要求

| 组件 | 最低版本 | 推荐版本 |
|------|---------|---------|
| Python | 3.9 | 3.10+ |
| pip | 21.0 | 23.0+ |
| 操作系统 | Windows / macOS / Linux | Ubuntu 22.04 LTS |
| 内存 | 4 GB | 8 GB+ |

### 1. 克隆仓库

```bash
git clone https://github.com/your-org/retail_analytics.git
cd retail_analytics
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 MiMo API（可选）

编辑 `config/settings.py`，填写您的 MiMo API 信息：

```python
MIMO_CONFIG = {
    "api_key": "your_api_key_here",
    "base_url": "https://api.mimo.example.com/v1",
    "model": "mimo-chat",
}
```

> 不配置 API 时，AI 助手将使用内置的模拟回答模式，不影响其他功能使用。

### 5. 启动系统

```bash
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501`，使用默认账号登录：

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |

### 6. 生成测试数据

登录后在侧边栏点击 **「🔄 生成模拟数据」**，系统将自动生成完整的测试数据集。

---

## 🏗️ 系统架构

### 分层架构设计

```
┌─────────────────────────────────────────────────────────┐
│                      展示层 (Presentation)                │
│   Streamlit Pages: 12 个页面模块                          │
│   ├── data_management    ├── data_overview               │
│   ├── behavior_analysis  ├── user_profiling              │
│   ├── prediction_models  ├── realtime_dashboard          │
│   ├── anomaly_detection  ├── ai_assistant                │
│   ├── pdf_export         ├── data_integration            │
│   └── system_management                                  │
├─────────────────────────────────────────────────────────┤
│                      业务逻辑层 (Business)                 │
│   utils/: 认证 / 数据处理 / PDF生成 / 性能优化              │
│   models/: MLP 购买意向预测 / LSTM 销售预测                 │
├─────────────────────────────────────────────────────────┤
│                       数据层 (Data)                       │
│   data/: 数据库操作 / 数据生成器 / 多源连接器                │
│   SQLite: retail.db (业务) + retail_analytics.db (认证)    │
├─────────────────────────────────────────────────────────┤
│                      基础设施层 (Infra)                    │
│   Docker / docker-compose / Nginx / Gunicorn              │
└─────────────────────────────────────────────────────────┘
```

### 数据流架构

```
数据源（CSV/Excel/API/JSON/DB）
        │
        ▼
  数据集成层 (data_connector)
        │
        ▼
  数据存储层 (SQLite - 5 张业务表)
        │
        ├──────────────────────────────────┐
        ▼                                  ▼
  数据处理引擎                       AI 模型引擎
  (data_processor)                  (purchase_intent + sales_forecast)
        │                                  │
        ├──────────────────────────────────┤
        ▼                                  ▼
  可视化渲染层 (Plotly)             AI 分析层 (MiMo API)
        │                                  │
        └──────────────┬───────────────────┘
                       ▼
              用户界面 (Streamlit)
```

### 数据库实体关系 (ER)

```
  users ──1:N──> orders ──1:N──> order_items ──N:1──> products
    │                                                    │
    └──────────1:N──> user_behavior ──N:1───────────────┘
```

5 张核心业务表：
- **users** — 用户信息（性别、年龄、城市、注册日期）
- **products** — 商品信息（名称、品类、价格、库存）
- **orders** — 订单记录（用户、日期、金额、状态）
- **order_items** — 订单明细（订单、商品、数量、单价）
- **user_behavior** — 行为日志（类型、时间、时长、设备、渠道）

---

## 📦 模块详解

### 核心模块一览

| 编号 | 模块 | 文件 | 核心职责 | 权限 |
|:---:|------|------|----------|:---:|
| M01 | 应用入口 | `app.py` | 路由分发、登录鉴权、侧边栏导航 | 全部 |
| M02 | 全局配置 | `config/settings.py` | 路径、API、模型、日志配置 | — |
| M03 | 数据库管理 | `data/database.py` | CRUD 封装、表初始化、批量插入 | — |
| M04 | 数据生成器 | `data/data_generator.py` | 模拟数据生成（5表联动） | — |
| M05 | 数据连接器 | `data/data_connector.py` | 多源数据接入（工厂模式） | — |
| M06 | 用户认证 | `utils/auth.py` | PBKDF2 密码哈希、RBAC 权限 | — |
| M07 | 数据处理 | `utils/data_processor.py` | 清洗、聚类、RFM、留存、漏斗 | — |
| M08 | PDF 生成 | `utils/pdf_generator.py` | WeasyPrint/ReportLab 双引擎 | — |
| M09 | 性能优化 | `utils/performance.py` | 缓存、WAL 模式、模型单例 | — |
| M10 | 购买预测 | `models/purchase_intent.py` | MLP + BatchNorm + Dropout + 早停 | — |
| M11 | 销售预测 | `models/sales_forecast.py` | 双 LSTM + 自回归滚动预测 | — |
| M12 | 数据管理 | `pages/data_management.py` | 上传/预览/清洗 3 子页面 | user+ |
| M13 | 数据概览 | `pages/data_overview.py` | 指标/趋势/画像 3 子页面 | user+ |
| M14 | 行为分析 | `pages/behavior_analysis.py` | 热力图/漏斗/留存/路径 4 子页面 | user+ |
| M15 | 用户画像 | `pages/user_profiling.py` | 聚类/生命周期 2 子页面 | user+ |
| M16 | 预测模型 | `pages/prediction_models.py` | 购买意向/销售预测 2 子页面 | user+ |
| M17 | AI 助手 | `pages/ai_assistant.py` | 智能问答/报告生成 2 子页面 | manager+ |
| M18 | 实时大屏 | `pages/realtime_dashboard.py` | 5秒刷新、指标卡、热销 TOP10 | user+ |
| M19 | 异常检测 | `pages/anomaly_detection.py` | Z-Score 检测、AI 诊断 | user+ |
| M20 | 系统管理 | `pages/system_management.py` | 用户管理/系统日志 | admin |

### 权限控制体系

```
admin (级别 3)
  ├── 可访问全部 12 个页面模块
  ├── 用户管理（创建/禁用/删除）
  ├── 系统日志查看
  └── 性能监控面板
        │
manager (级别 2)
  ├── 可访问 10 个页面模块
  ├── AI 助手（智能问答 + 报告生成）
  ├── 数据集成（多源导入）
  └── 模拟数据生成
        │
user (级别 1)
  ├── 可访问 8 个页面模块
  ├── 数据管理、概览、行为分析
  ├── 用户画像、预测模型
  └── 实时监控、异常检测
```

---

## 🔧 技术栈

| 类别 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **Web 框架** | Streamlit | ≥1.30.0 | 全栈 Web UI，声明式组件渲染 |
| **UI 组件** | streamlit-antd-components | ≥0.2.0 | Ant Design 风格侧边栏菜单 |
| **数据处理** | Pandas + NumPy | ≥2.0.0 / ≥1.24.0 | 数据清洗、转换、统计分析 |
| **可视化** | Plotly | ≥5.15.0 | 交互式图表（热力图/漏斗/桑基图/雷达图） |
| **机器学习** | Scikit-learn | ≥1.3.0 | K-Means 聚类、RFM 分位数分析 |
| **深度学习** | PyTorch + TorchVision | ≥2.0.0 | MLP 购买意向预测、LSTM 销售预测 |
| **数据库** | SQLite | 内置 | 轻量级关系型数据库，WAL 模式 |
| **AI 大模型** | MiMo API（OpenAI 兼容） | — | 智能问答、报告生成、异常诊断 |
| **PDF 生成** | WeasyPrint / ReportLab | — | HTML→PDF / 原生 PDF 双引擎 |
| **容器化** | Docker + docker-compose | — | 应用容器化，Nginx 反向代理 |
| **监控** | Grafana + Redis | — | 性能监控面板、缓存加速 |
| **部署** | Gunicorn | ≥21.0.0 | WSGI 生产级服务器 |
| **Excel** | openpyxl + xlrd | ≥3.1.0 / ≥2.0.0 | Excel 读写与报告导出 |
| **性能** | psutil | ≥5.9.0 | 系统资源监控 |

---

## 🐳 部署指南

### Docker 部署（推荐）

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f app
```

`docker-compose.yml` 包含 4 个核心服务：

| 服务 | 端口 | 说明 |
|------|------|------|
| app | 8501 | Streamlit 应用主服务 |
| nginx | 80 | 反向代理 + Gzip 压缩 + 限流 |
| mysql | 3306 | 可选的关系型数据库替代 |
| redis | 6379 | 缓存服务 |

### 手动部署

```bash
# 安装 Gunicorn
pip install gunicorn

# 生产模式启动
gunicorn -w 4 -b 0.0.0.0:8501 app:app

# 配置 Nginx 反向代理
sudo cp nginx/nginx.conf /etc/nginx/sites-available/retail-analytics
sudo ln -s /etc/nginx/sites-available/retail-analytics /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 一键启动（Windows）

双击项目根目录下的 `一键启动.bat`，自动完成环境检查和应用启动。

---

## 📊 模型详情

### 购买意向预测 (MLP)

```
PurchaseIntentModel:
  Input(12+ features) → Linear(128) → BatchNorm1d → ReLU → Dropout(0.3)
                      → Linear(64)  → BatchNorm1d → ReLU → Dropout(0.2)
                      → Linear(32)  → BatchNorm1d → ReLU → Dropout(0.1)
                      → Linear(1)   → Sigmoid → Output(0~1)
```

- **损失函数**：BCE Loss
- **优化器**：Adam (lr=0.001, weight_decay=1e-5)
- **训练策略**：早停 patience=10，ReduceLROnPlateau
- **评估指标**：Accuracy / AUC / F1-Score / Precision / Recall

### 销售预测 (LSTM)

```
LSTMSalesForecast:
  Input(seq_len, 1) → LSTM(64, layer=1, batch_first) → Dropout(0.2)
                    → LSTM(64, layer=2, batch_first) → Dropout(0.2)
                    → Linear(64, 1) → Output
```

- **损失函数**：MSE Loss
- **优化器**：Adam
- **评估指标**：MAE / RMSE
- **预测方式**：滑动窗口自回归（用预测值继续预测下一步）

---

## 📁 项目结构

```
retail_analytics/
├── .streamlit/
│   └── config.toml                 # Streamlit 服务端配置（端口/主题/CORS）
├── config/
│   └── settings.py                 # 全局配置中心（路径/API/模型/日志）
├── data/
│   ├── __init__.py                 # 数据层模块导出
│   ├── database.py                 # 数据库初始化、CRUD 操作封装
│   ├── data_generator.py           # 模拟数据生成器（5 表联动）
│   ├── data_connector.py           # 多数据源连接器（工厂模式）
│   ├── retail.db                   # 业务数据库
│   └── retail_analytics.db         # 认证系统数据库
├── models/
│   ├── purchase_intent.py          # MLP 购买意向预测（PyTorch）
│   └── sales_forecast.py           # LSTM 销售预测（PyTorch）
├── pages/
│   ├── __init__.py                 # 页面模块导出
│   ├── data_management.py          # 数据管理（上传/预览/清洗）
│   ├── data_overview.py            # 数据概览（指标/趋势/画像）
│   ├── behavior_analysis.py        # 行为分析（热力图/漏斗/留存/路径）
│   ├── user_profiling.py           # 用户画像（聚类/生命周期）
│   ├── prediction_models.py        # 预测模型（购买意向/销售预测）
│   ├── realtime_dashboard.py       # 实时数据大屏（5秒刷新）
│   ├── anomaly_detection.py        # 异常检测播报（Z-Score）
│   ├── ai_assistant.py             # AI 助手（智能问答/报告生成）
│   ├── pdf_export.py               # PDF 报告导出
│   ├── data_integration.py         # 数据集成（CSV/Excel/API/DB）
│   └── system_management.py        # 系统管理（用户管理/日志）
├── utils/
│   ├── __init__.py                 # 工具模块导出
│   ├── auth.py                     # 用户认证与权限管理（RBAC）
│   ├── data_processor.py           # 数据处理引擎（清洗/聚类/RFM/留存）
│   ├── pdf_generator.py            # PDF 报告生成（WeasyPrint/ReportLab）
│   └── performance.py              # 性能优化（缓存/WAL/模型单例）
├── deploy/
│   ├── README.md                   # 部署详细指南
│   └── start.sh                    # Linux 启动脚本
├── nginx/
│   └── nginx.conf                  # Nginx 反向代理配置
├── app.py                          # 主入口（路由/鉴权/导航）
├── Dockerfile                      # Docker 镜像构建
├── docker-compose.yml              # 多服务编排（App+Nginx+MySQL+Redis）
├── requirements.txt                # Python 依赖清单
├── 一键启动.bat                     # Windows 一键启动脚本
└── README.md                       # 项目说明文档
```

---

## 📝 开发路线图

### ✅ 第一期（已完成）
- 数据管理（上传 / 预览 / 清洗）
- 数据概览（指标 / 趋势 / 画像）
- 行为分析（热力图 / 漏斗 / 留存 / 路径）
- 用户画像（RFM / K-Means 聚类 / 生命周期）
- AI 助手（智能问答 / 报告生成）

### ✅ 第二期（已完成）
- PyTorch 购买意向预测模型（MLP）
- LSTM 销售预测模型
- 实时监控大屏（5 秒刷新）
- 异常检测播报（Z-Score + AI 诊断）
- PDF 报告导出
- Docker 容器化部署
- 多数据源集成（CSV / Excel / JSON / API / DB）
- 系统管理（用户管理 / 日志）

### ⬜ 第三期（规划中）
- 亮色 / 暗色主题切换
- 中英文国际化
- 云端部署与 CI/CD
- 数据看板自定义配置
- 邮件 / 钉钉告警推送

---

## ❓ 常见问题

<details>
<summary><b>1. 如何获取 MiMo API Key？</b></summary>

访问小米 AI 开放平台申请 API Key，在 `config/settings.py` 中配置即可。不配置时系统会自动降级为模拟回答模式，不影响其他功能。
</details>

<details>
<summary><b>2. 数据库表结构是怎样的？</b></summary>

系统包含 5 张业务表（users / products / orders / order_items / user_behavior）+ 2 张认证表（auth_users / user_sessions）。详细设计见项目文档中的《数据库设计文档》。
</details>

<details>
<summary><b>3. 如何添加新的分析页面？</b></summary>

1. 在 `pages/` 目录下创建新的 Python 文件
2. 定义页面函数（接收 `st` 参数）
3. 在 `app.py` 的 `main()` 函数中添加路由分支
4. 在 `sidebar_navigation()` 中配置菜单项和权限
</details>

<details>
<summary><b>4. 模型训练需要 GPU 吗？</b></summary>

不需要。MLP 和 LSTM 模型的数据量较小（数千条记录），CPU 即可完成训练，通常在 30 秒内完成。
</details>

<details>
<summary><b>5. 支持哪些数据源接入？</b></summary>

支持 CSV 文件（自动编码检测）、Excel 文件（多 Sheet）、JSON 文件、REST API（GET/POST）、SQLite 数据库 5 种数据源。
</details>

---


---

## 📄 许可证

本项目仅供学习和研究使用。

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

</div>
