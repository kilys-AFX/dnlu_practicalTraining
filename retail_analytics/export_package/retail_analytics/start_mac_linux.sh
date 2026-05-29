#!/bin/bash
# 智能零售分析系统 - Mac/Linux 启动脚本

echo "================================================"
echo "    智能零售用户行为分析系统 - 启动器"
echo "================================================"
echo

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    echo "访问: https://www.python.org/downloads/"
    echo
    read -p "按回车键退出..."
    exit 1
fi

echo "[1/5] 检查 Python 环境..."
python3 --version

echo
echo "[2/5] 安装/更新依赖包..."
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

if [ $? -ne 0 ]; then
    echo
    echo "[警告] 依赖安装可能不完整，是否继续？(Y/N)"
    read -p "> " choice
    if [ "$choice" != "Y" ] && [ "$choice" != "y" ]; then
        echo "退出安装"
        exit 1
    fi
fi

echo
echo "[3/5] 检查数据目录..."
if [ ! -f "data/retail_analytics.db" ]; then
    echo "- 数据库不存在，将在首次运行时自动创建"
fi

# 创建必要目录
mkdir -p data assets logs

echo
echo "[4/5] 启动系统..."
echo "- 系统地址: http://localhost:8501"
echo "- 默认账号: admin"
echo "- 默认密码: admin123"
echo
echo "================================================"
echo "正在启动，请稍候..."
echo "首次启动可能需要 1-2 分钟，请耐心等待"
echo "================================================"
echo

# 启动 Streamlit
streamlit run app.py --server.port 8501 --server.address localhost

# 如果启动失败
if [ $? -ne 0 ]; then
    echo
    echo "[错误] 系统启动失败"
    echo "请检查："
    echo "  1. 依赖是否全部安装成功"
    echo "  2. 端口 8501 是否被占用"
    echo "  3. Python 版本是否 >= 3.8"
    echo
    read -p "按回车键退出..."
    exit 1
fi

read -p "按回车键退出..."
