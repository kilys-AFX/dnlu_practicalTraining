# MySQL 数据库切换说明

## 已完成的工作

### 1. 安装依赖
✅ 已安装 `PyMySQL` 连接器

### 2. 修改配置文件
✅ 已更新 `config/settings.py`，添加 MySQL 配置选项

### 3. 重写数据库模块
✅ 已重写 `data/database.py`，支持 SQLite 和 MySQL 两种数据库

## 您需要完成的步骤

### 步骤 1：安装并启动 MySQL 服务器

1. **下载 MySQL**：
   - 访问：https://dev.mysql.com/downloads/mysql/
   - 下载 MySQL Community Server（免费版）

2. **安装 MySQL**：
   - 按照安装向导进行安装
   - 记住您设置的 `root` 用户密码

3. **启动 MySQL 服务**：
   - Windows：在"服务"中启动 MySQL 服务
   - 或使用命令：`net start mysql`

### 步骤 2：配置 MySQL 连接信息

编辑 `config/settings.py` 文件，填写您的 MySQL 连接信息：

```python
# MySQL 配置（切换到 MySQL 时需要填写）
MYSQL_CONFIG = {
    "host": "localhost",        # MySQL 服务器地址（默认 localhost）
    "port": 3306,              # MySQL 端口（默认 3306）
    "user": "root",             # MySQL 用户名（默认 root）
    "password": "your_password", # 替换为您的 MySQL 密码
    "database": "retail_analytics",  # 数据库名称（会自动创建）
    "charset": "utf8mb4"
}

# 使用数据库类型：'sqlite' 或 'mysql'
DB_TYPE = "mysql"  # 改为 "mysql" 启用 MySQL
```

### 步骤 3：初始化 MySQL 数据库

在命令行中运行：

```bash
cd d:\codebuddy\education\retail_analytics
python -c "from data.database import init_database; init_database()"
```

这会：
1. 创建 `retail_analytics` 数据库
2. 创建所有必需的表（users, products, orders, order_items, user_behavior）

### 步骤 4：生成测试数据（可选）

如果您需要测试数据，运行：

```bash
python -c "from data.data_generator import generate_all_data; generate_all_data()"
```

### 步骤 5：启动应用

```bash
streamlit run app.py
```

## 切换回 SQLite

如果您想切换回 SQLite，只需修改 `config/settings.py`：

```python
DB_TYPE = "sqlite"  # 改回 "sqlite"
```

## 常见问题

### 1. 连接 MySQL 失败
- 检查 MySQL 服务是否启动
- 检查密码是否正确
- 检查端口是否被占用（默认 3306）

### 2. 找不到模块 `pymysql`
运行：`pip install pymysql`

### 3. 权限错误
确保 MySQL 用户有创建数据库的权限

## 技术细节

### 数据库兼容性处理

代码已处理以下兼容性问题：

1. **自增语法**：
   - SQLite：`AUTOINCREMENT`
   - MySQL：`AUTO_INCREMENT`

2. **清空表**：
   - SQLite：`DELETE FROM table`
   - MySQL：`TRUNCATE TABLE table`

3. **查看表结构**：
   - SQLite：`PRAGMA table_info(table)`
   - MySQL：`DESCRIBE table`

4. **检查表是否存在**：
   - SQLite：`SELECT name FROM sqlite_master...`
   - MySQL：`SHOW TABLES LIKE 'table'`

### 数据结构

MySQL 数据库使用以下引擎和字符集：
- 引擎：`InnoDB`（支持外键）
- 字符集：`utf8mb4`（支持 emoji）

## 下一步

完成上述配置后，您的应用将使用 MySQL 数据库。所有现有功能（用户管理、数据分析、预测模型等）都应该正常工作。
