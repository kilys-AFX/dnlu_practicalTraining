#!/bin/bash
# 零售分析系统 - 启动脚本（Linux/macOS）
# 作者: AI研究生
# 日期: 2026-05-29

echo "=========================================="
echo "零售分析系统 - 启动脚本"
echo "=========================================="
echo ""

# 检查Python版本
echo "[1/5] 检查Python版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3 未安装，请先安装Python 3.8+"
    exit 1
fi
echo "✅ Python版本检查通过"
echo ""

# 检查pip
echo "[2/5] 检查pip..."
pip3 --version
if [ $? -ne 0 ]; then
    echo "❌ pip3 未安装，请先安装pip"
    exit 1
fi
echo "✅ pip版本检查通过"
echo ""

# 安装依赖
echo "[3/5] 安装依赖..."
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi
echo "✅ 依赖安装完成"
echo ""

# 初始化数据库
echo "[4/5] 初始化数据库..."
python3 -c "from data.database import init_db; init_db()"
if [ $? -ne 0 ]; then
    echo "⚠️ 数据库初始化失败，但将继续启动"
fi
echo ""

# 启动系统
echo "[5/5] 启动系统..."
echo "系统将在浏览器中自动打开..."
echo "如果没有自动打开，请手动访问: http://localhost:8501"
echo ""
echo "按 Ctrl+C 停止系统"
echo ""

streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true