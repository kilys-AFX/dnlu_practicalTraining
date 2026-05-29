@echo off
chcp 65001 > nul
echo ==========================================
echo 零售分析系统 - 中文界面修复版
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查依赖...
python -c "import streamlit; import pandas; import plotly; print('✅ 核心依赖正常')"

echo.
echo [2/3] 启动系统...
echo 系统将在浏览器中自动打开...
echo 如果没有自动打开，请手动访问: http://localhost:8501
echo.
echo [3/3] 正在启动...
python -m streamlit run app.py --server.port 8501 --server.headless true

pause
