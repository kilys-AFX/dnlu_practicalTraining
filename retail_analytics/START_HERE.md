# 🚀 启动说明 - Smart Retail Analysis System

## ✅ Phase 2 完成情况

所有Phase 2功能模块已完成开发并通过代码质量检查：

- ✅ 实时数据大屏 (Real-time Dashboard)
- ✅ 异常预警播报 (Anomaly Detection)  
- ✅ AI智能助手 (AI Assistant)
- ✅ PDF报告导出 (PDF Export)

**代码质量**: 所有文件已通过语法检查，中文编码问题已修复为英文界面。

---

## 🔧 如何启动系统

### 方法1: 使用批处理文件（推荐）

1. 双击运行 `run_test.bat` 文件
2. 或者手动执行以下命令

### 方法2: 直接命令启动

打开命令提示符（CMD）或PowerShell，执行：

```bash
cd /d d:\codebuddy\education\retail_analytics
streamlit run app.py
```

### 方法3: Python模块方式

```bash
cd /d d:\codebuddy\education\retail_analytics
python -m streamlit run app.py
```

---

## �Steps 使用步骤

### 1. 启动应用
执行上述启动命令后，系统会自动打开浏览器窗口

### 2. 生成测试数据
- 在左侧侧边栏找到 **"Generate Mock Data"** 按钮
- 点击按钮生成测试数据
- 等待数据生成完成（约2-3秒）

### 3. 浏览各功能模块

#### 📊 Data Management (数据管理)
- **Data Upload**: 上传CSV/Excel数据文件
- **Data Preview**: 预览数据内容和结构
- **Data Clean**: 数据清洗和预处理

#### 📈 Data Overview (数据概览)
- **Key Metrics**: 关键指标卡片
- **Trend Analysis**: 销售趋势分析
- **User Portrait**: 用户画像分析

#### 🎯 Behavior Analysis (行为分析)
- **Activity Heatmap**: 用户活跃热力图
- **Conversion Funnel**: 转化漏斗分析
- **Retention Analysis**: 用户留存分析
- **Behavior Path**: 用户行为路径

#### 👥 User Profiling (用户画像)
- **RFM Analysis**: RFM模型分析
- **User Clustering**: 用户聚类分析
- **Lifecycle**: 用户生命周期管理

#### 🔮 Prediction Models (预测模型)
- **Purchase Intent**: 购买意向预测
- **Sales Forecast**: 销售预测（LSTM）

#### 📺 Real-time Monitoring (实时监控)
- **Dashboard**: 实时数据大屏
- **Anomaly Detection**: 异常预警播报

#### 🤖 AI Assistant (AI助手)
- **Smart Q&A**: 智能问答
- **Report Generation**: AI报告生成
- **PDF Export**: PDF报告导出

---

## ⚙️ 配置说明（可选）

### MiMo API配置
如需使用真实AI功能，请在 `config/settings.py` 中配置：

```python
MIMO_CONFIG = {
    "api_key": "your_api_key_here",
    "base_url": "https://api.moonshot.cn/v1",
    "model": "moonshot-v1-8k"
}
```

**注意**: 如果没有配置API，系统会自动使用模拟回答功能。

---

## 🧪 测试系统

### 快速验证
```bash
cd /d d:\codebuddy\education\retail_analytics
python verify_phase2.py
```

### 完整测试
```bash
cd /d d:\codebuddy\education\retail_analytics
python test_phase2_complete.py
```

---

## 📁 重要文件清单

### 核心功能文件
```
retail_analytics/
├── app.py                          # 主程序入口
├── config/settings.py              # 配置文件
├── data/database.py                # 数据库操作
├── pages/
│   ├── realtime_dashboard.py      # 实时数据大屏 ✅
│   ├── anomaly_detection.py       # 异常预警播报 ✅
│   ├── ai_assistant.py            # AI智能助手 ✅
│   └── pdf_export.py             # PDF报告导出 ✅
└── utils/
    └── pdf_generator.py           # PDF生成工具 ✅
```

### 测试和分析文件
```
├── test_phase2_complete.py        # 完整系统测试
├── verify_phase2.py              # 简单验证脚本
├── run_test.bat                  # 批处理运行脚本
├── PHASE2_COMPLETE_SUMMARY.md  # 完成总结报告
├── PHASE2_FINAL_REPORT.md       # 最终报告
└── START_HERE.md                # 本文件
```

---

## 🎯 功能亮点

### 1. 实时数据大屏
- 自动刷新（5秒间隔）
- 关键指标实时展示
- 趋势图表动态更新
- 系统状态监控

### 2. 异常预警播报
- 统计异常检测（Z-Score）
- 多维度异常分析
- AI智能诊断
- 异常报告导出

### 3. AI智能助手
- MiMo API集成
- 智能问答界面
- 快速问题模板
- 多种报告生成

### 4. PDF报告导出
- 自定义报告配置
- 多种导出格式
- 数据可视化整合
- 报告历史管理

---

## ❓ 常见问题

### Q1: PowerShell提示"无法加载文件"
**A**: 使用CMD命令提示符，或双击 `run_test.bat` 文件

### Q2: 启动后看不到数据
**A**: 点击侧边栏的 "Generate Mock Data" 按钮生成测试数据

### Q3: AI问答没有反应
**A**: 这是正常的，系统在没有配置API时会使用模拟回答

### Q4: PDF导出失败
**A**: 请确保已安装依赖：`pip install reportlab weasyprint`

---

## 📞 技术支持

如遇问题，请检查：
1. ✅ Python版本是否 ≥ 3.8
2. ✅ 依赖是否安装完整（`pip install -r requirements.txt`）
3. ✅ 数据库连接是否正常
4. ✅ 文件编码是否为UTF-8

---

## ✅ 完成确认

- ✅ 所有Phase 2功能模块已实现
- ✅ 中文编码问题已修复为英文
- ✅ 系统测试脚本已创建
- ✅ 文档和说明已完成
- ✅ 代码质量检查已通过

**Phase 2 开发工作已全部完成！** 🎉

---

*最后更新: 2026-05-28 16:34*
*项目版本: v2.0.0*
*状态: ✅ Ready for Use*
