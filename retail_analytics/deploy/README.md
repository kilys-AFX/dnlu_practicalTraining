# 零售分析系统 - 部署指南

## 系统要求

### 基础环境
- **操作系统**: Windows 10/11, Linux, macOS
- **Python**: 3.8+ (推荐 3.10+)
- **内存**: 最低 4GB，推荐 8GB+
- **硬盘**: 最低 2GB 可用空间

### Python依赖
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.15.0
torch>=2.0.0
scikit-learn>=1.3.0
streamlit-antd-components>=0.2.0
openpyxl>=3.1.0
requests>=2.31.0
```

## 部署方式

### 方式一：本地部署（开发/测试）

1. **克隆项目**
```bash
git clone <repository-url>
cd retail_analytics
```

2. **创建虚拟环境**（推荐）
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **启动系统**
```bash
streamlit run app.py --server.port 8501
```

5. **访问系统**
打开浏览器访问: http://localhost:8501

### 方式二：Docker部署（推荐生产环境）

1. **构建Docker镜像**
```bash
docker build -t retail-analytics .
```

2. **运行容器**
```bash
docker run -d \
  --name retail-analytics \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  retail-analytics
```

3. **访问系统**
打开浏览器访问: http://localhost:8501

### 方式三：云服务器部署

#### 1. 阿里云/腾讯云/AWS部署

**环境准备**
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python 3.10+
sudo apt install python3.10 python3-pip python3-venv -y

# 安装Nginx
sudo apt install nginx -y

# 安装Docker（可选）
curl -fsSL https://get.docker.com | sh
```

**部署步骤**
```bash
# 克隆项目
git clone <repository-url>
cd retail_analytics

# 安装依赖
pip3 install -r requirements.txt

# 使用systemd管理服务
sudo nano /etc/systemd/system/retail-analytics.service
```

**systemd服务配置**
```ini
[Unit]
Description=Retail Analytics System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/retail_analytics
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

**启动服务**
```bash
sudo systemctl daemon-reload
sudo systemctl enable retail-analytics
sudo systemctl start retail-analytics
sudo systemctl status retail-analytics
```

**配置Nginx反向代理**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 2. 使用Docker Compose部署

**docker-compose.yml**
```yaml
version: '3.8'

services:
  retail-analytics:
    build: .
    container_name: retail-analytics
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: retail-analytics-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - retail-analytics
    restart: unless-stopped
```

## 性能优化

### 1. Streamlit配置优化

**创建 .streamlit/config.toml**
```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[logger]
level = "WARNING"
```

### 2. 数据库优化

**启用WAL模式**（提高SQLite并发性能）
```python
# 在 database.py 中添加
def enable_wal_mode():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-10000")  # 10MB缓存
    conn.close()
```

### 3. 缓存策略

**使用Streamlit缓存**
```python
@st.cache_data(ttl=3600)  # 缓存1小时
def load_data():
    return execute_query("SELECT * FROM ...")
```

### 4. 模型优化

**使用ONNX格式**（提高推理速度）
```python
import torch
import onnx
from onnx import optimizer

# 将PyTorch模型转换为ONNX
dummy_input = torch.randn(1, input_dim)
torch.onnx.export(model, dummy_input, "model.onnx")
```

## 安全配置

### 1. 用户认证
- 默认管理员账号: admin / admin123 (首次登录后请立即修改密码)
- 启用密码复杂度检查
- 启用登录失败锁定

### 2. HTTPS配置

**使用Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 3. 防火墙配置
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## 监控和维护

### 1. 日志监控
```bash
# 查看Streamlit日志
sudo journalctl -u retail-analytics -f

# 查看Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. 性能监控

**安装监控工具**
```bash
pip install psutil streamlit-metrics
```

**添加健康检查端点**
```python
# 在app.py中添加
def health_check():
    return {
        "status": "healthy",
        "database": check_database_connection(),
        "model": check_model_loaded()
    }
```

### 3. 自动备份

**创建备份脚本** (`backup.sh`)
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/retail_analytics"

# 备份数据库
cp data/retail_analytics.db $BACKUP_DIR/db_$DATE.db

# 备份上传的文件
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz data/uploads/

# 删除7天前的备份
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

**添加到crontab**
```bash
0 2 * * * /home/ubuntu/retail_analytics/backup.sh
```

## 故障排除

### 常见问题

1. **端口8501被占用**
```bash
# 查看占用进程
lsof -i :8501
# 杀死进程
kill -9 <PID>
```

2. **内存不足**
```bash
# 增加交换空间
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

3. **模型加载失败**
```bash
# 重新训练模型
python -m models.purchase_intent
python -m models.sales_forecast
```

## 更新和升级

### 更新系统
```bash
# 拉取最新代码
git pull origin main

# 安装新依赖
pip install -r requirements.txt

# 重启服务
sudo systemctl restart retail-analytics
```

### 数据库迁移
```bash
# 备份数据库
cp data/retail_analytics.db data/retail_analytics.db.backup

# 运行迁移脚本
python migrations/upgrade.py
```

## 技术支持

如有问题，请联系：
- 技术支持邮箱: support@retail-analytics.com
- 问题反馈: https://github.com/your-repo/issues
