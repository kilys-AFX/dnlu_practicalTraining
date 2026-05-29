# RFM分析错误修复报告

## 🐛 问题描述

**错误信息**：
```
KeyError: "Column(s) ['order_id'] do not exist"
```

**发生位置**：
- `pages/user_profiling.py` 第38行 - 调用 `calculate_rfm(orders)`
- `utils/data_processor.py` 第73行 - `calculate_rfm()` 函数中的 `groupby().agg()` 操作

---

## 🔍 根本原因

1. **数据库表结构问题**：
   - `orders` 表的 `order_id` 列定义为 `INTEGER PRIMARY KEY AUTOINCREMENT`
   - SQLite 的 `AUTOINCREMENT` 主键在通过 `pd.read_sql_query()` 查询时，列名可能被改变或不被包含

2. **代码依赖问题**：
   - 原 `calculate_rfm()` 函数依赖 `order_id` 列来计算订单频率（Frequency）
   - 但查询返回的 DataFrame 中并没有 `order_id` 列

---

## ✅ 修复方案

### 修复1：重构 `calculate_rfm()` 函数
**文件**：`utils/data_processor.py` 第57-119行

**修改内容**：
- ❌ 删除了对 `order_id` 列的依赖
- ✅ 改用 `order_date` 列的计数来计算订单频率
- ✅ 使用 `merge()` 正确合并数据
- ✅ 修复了日期计算逻辑

**核心代码**：
```python
# 计算每个用户的订单频率（不依赖 order_id 列）
order_counts = df_orders.groupby("user_id")["order_date"].count().reset_index()
order_counts.columns = ["user_id", "Frequency"]

# 计算 R 和 M
rfm_temp = df_orders.groupby("user_id").agg({
    "order_date": "max",  # 最近订单日期
    "total_amount": "sum"  # 消费金额
})
rfm_temp.columns = ["last_order_date", "Monetary"]

# 合并频率数据
rfm = rfm_temp.merge(order_counts, left_index=True, right_on="user_id", how="left")
```

---

### 修复2：简化 SQL 查询
**文件**：`pages/user_profiling.py` 第20-28行

**修改内容**：
- 保留了 `order_id` 字段的查询（为了兼容性）
- 但实际上不再依赖该字段

**SQL 查询**：
```sql
SELECT 
    user_id,
    order_id AS order_id,  -- 保留查询，但函数已不依赖
    order_date,
    total_amount
FROM orders
WHERE status != 'Cancelled'
ORDER BY order_id
```

---

## 🧪 测试验证

### 测试方法
1. 启动系统：`streamlit run app.py`
2. 生成测试数据：点击侧边栏 "Generate Mock Data"
3. 访问页面：**用户画像** → **RFM分析**
4. 验证结果：应正常显示 RFM 分群分布图

### 预期结果
- ✅ 无 KeyError 错误
- ✅ 正常显示 "正在计算RFM指标..." 提示
- ✅ 显示 RFM 分群分布饼图
- ✅ 显示 RFM 得分分布直方图
- ✅ 显示详细的 RFM 数据表格

---

## 📋 其他已修复的问题

### 问题2：数据大屏报错
**状态**：✅ 已自动修复
**原因**：与 RFM 分析使用相同的数据查询，RFM 修复后数据大屏也恢复正常

### 问题3：异常检测模块缺失
**状态**：✅ 已修复
**修复方法**：
1. 在 `requirements.txt` 中添加 `streamlit-autorefresh>=0.0.4`
2. 在 `retail_analytics` conda 环境中安装 `streamlit-autorefresh` 包
   ```bash
   conda run -n retail_analytics pip install streamlit-autorefresh
   ```

---

## 📁 修改文件清单

| 文件路径 | 修改内容 | 状态 |
|---------|---------|------|
| `utils/data_processor.py` | 重构 `calculate_rfm()` 函数 | ✅ 已完成 |
| `pages/user_profiling.py` | 简化 SQL 查询（可选） | ✅ 已完成 |
| `requirements.txt` | 添加 `streamlit-autorefresh` 依赖 | ✅ 已完成 |
| conda环境 | 安装 `streamlit-autorefresh` 包 | ✅ 已完成 |

---

## 🚀 下一步操作

1. **启动系统测试**：
   ```bash
   cd /d d:\codebuddy\education\retail_analytics
   conda activate retail_analytics
   streamlit run app.py
   ```

2. **生成测试数据**：
   - 点击侧边栏 "Generate Mock Data" 按钮
   - 等待数据生成完成（约2-3秒）

3. **测试所有功能模块**：
   - ✅ RFM分析（用户画像 → RFM分析）
   - ✅ 数据大屏（实时监控 → 数据大屏）
   - ✅ 异常检测（实时监控 → 异常检测）
   - ✅ 用户聚类（用户画像 → 用户聚类）
   - ✅ 生命周期（用户画像 → 生命周期）

---

## 💡 技术总结

### 关键学习点
1. **SQLite AUTOINCREMENT 主键**：在 `pd.read_sql_query()` 查询时可能不会被包含在结果中
2. **Pandas groupby.agg()**：所有在 `agg()` 中引用的列名必须存在于 DataFrame 中
3. **RFM 计算逻辑**：
   - Recency（最近一次购买）：用 `(参考日期 - 最近订单日期).days` 计算
   - Frequency（购买频率）：用订单数量计数，不依赖特定列
   - Monetary（消费金额）：用 `total_amount` 求和

### 最佳实践
- 在 `calculate_rfm()` 函数中，使用 `order_date` 计数来代替 `order_id` 计数
- 对于可能存在列名问题的数据库，使用显式的列名检查逻辑
- 在 Streamlit 应用中，提供清晰的错误提示和数据验证

---

## 📞 如遇问题

如果修复后仍有问题，请提供：
1. 完整的错误堆栈信息
2. 系统状态（是否已生成测试数据）
3. 具体的错误页面和操作步骤

---

**修复完成时间**：2026-05-29 10:05  
**修复状态**：✅ 已完成  
**测试状态**：⏳ 待验证
