@echo off
chcp 65001 >nul
title 环境配置工具

echo ================================================
echo    智能零售分析系统 - 环境配置
echo ================================================
echo.

echo [1] 检查 Python 版本...
python --version
if %errorlevel% neq 0 (
    echo [错误] 请先安装 Python 3.8 或更高版本
    pause
    exit /b 1
)

echo.
echo [2] 升级 pip...
python -m pip install --upgrade pip

echo.
echo [3] 安装依赖包（使用清华镜像源）...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [4] 验证安装...
python -c "import streamlit, pandas, numpy, plotly, sklearn; print('✓ 核心依赖安装成功')"

echo.
echo [5] 创建必要目录...
if not exist "data" mkdir data
if not exist "assets" mkdir assets
if not exist "logs" mkdir logs

echo.
echo ================================================
echo 环境配置完成！
echo.
echo 接下来可以：
echo   1. 双击"一键启动.bat"启动系统
echo   2. 或手动运行: streamlit run app.py
echo ================================================
echo.

pause
