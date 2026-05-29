@echo off
chcp 65001 >nul
title 智能零售分析系统 - 一键启动

echo ================================================
echo    智能零售用户行为分析系统 - 启动器
echo ================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/4] 检查 Python 环境...
python --version

echo.
echo [2/4] 安装/更新依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [3/4] 检查数据目录...
if not exist "data\retail_analytics.db" (
    echo - 数据库不存在，将在首次运行时自动创建
)

echo.
echo [4/4] 启动系统...
echo - 系统地址: http://localhost:8501
echo - 默认账号: admin
echo - 默认密码: admin123
echo.
echo ================================================
echo 正在启动，请稍候...
echo 首次启动可能需要 1-2 分钟，请耐心等待
echo ================================================
echo.

streamlit run app.py --server.port 8501 --server.address localhost

pause
