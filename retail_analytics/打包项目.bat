@echo off
chcp 65001 >nul
title 项目打包工具

echo ================================================
echo    智能零售分析系统 - 项目打包
echo ================================================
echo.

set PROJECT_NAME=retail_analytics
set EXPORT_DIR=export_package

echo [1/5] 创建导出目录...
if exist "%EXPORT_DIR%" rmdir /s /q "%EXPORT_DIR%"
mkdir "%EXPORT_DIR%\%PROJECT_NAME%"

echo.
echo [2/5] 复制核心文件...
xcopy /E /I /Y "app.py" "%EXPORT_DIR%\%PROJECT_NAME%\"
xcopy /E /I /Y "requirements.txt" "%EXPORT_DIR%\%PROJECT_NAME%\"
xcopy /E /I /Y "README.md" "%EXPORT_DIR%\%PROJECT_NAME%\"
xcopy /E /I /Y "部署说明.md" "%EXPORT_DIR%\%PROJECT_NAME%\"
xcopy /E /I /Y "一键启动.bat" "%EXPORT_DIR%\%PROJECT_NAME%\"
xcopy /E /I /Y "环境配置.bat" "%EXPORT_DIR%\%PROJECT_NAME%\"

echo.
echo [3/5] 复制代码目录...
xcopy /E /I /Y "config" "%EXPORT_DIR%\%PROJECT_NAME%\config\"
xcopy /E /I /Y "data" "%EXPORT_DIR%\%PROJECT_NAME%\data\"
xcopy /E /I /Y "pages" "%EXPORT_DIR%\%PROJECT_NAME%\pages\"
xcopy /E /I /Y "utils" "%EXPORT_DIR%\%PROJECT_NAME%\utils\"
xcopy /E /I /Y "models" "%EXPORT_DIR%\%PROJECT_NAME%\models\"
xcopy /E /I /Y "assets" "%EXPORT_DIR%\%PROJECT_NAME%\assets\"
xcopy /E /I /Y "deploy" "%EXPORT_DIR%\%PROJECT_NAME%\deploy\"

echo.
echo [4/5] 清理临时文件...
del /s /q "%EXPORT_DIR%\%PROJECT_NAME%\*.pyc" 2>nul
del /s /q "%EXPORT_DIR%\%PROJECT_NAME%\__pycache__" 2>nul
del /s /q "%EXPORT_DIR%\%PROJECT_NAME%\*.db" 2>nul
del /s /q "%EXPORT_DIR%\%PROJECT_NAME%\*.log" 2>nul

echo.
echo [5/5] 创建快速开始指南...
(
echo # 快速开始指南
echo.
echo ## 1. 安装 Python
echo 下载并安装 Python 3.8 或更高版本：https://www.python.org/downloads/
echo.
echo ## 2. 配置环境
echo 双击运行 "环境配置.bat"
echo.
echo ## 3. 启动系统
echo 双击运行 "一键启动.bat"
echo.
echo ## 4. 访问系统
echo 浏览器打开：http://localhost:8501
echo 默认账号：admin
echo 默认密码：admin123
echo.
echo ## 详细文档
echo 请查看 "部署说明.md"
) > "%EXPORT_DIR%\%PROJECT_NAME%\快速开始.txt"

echo.
echo ================================================
echo 打包完成！
echo.
echo 导出位置：%EXPORT_DIR%\%PROJECT_NAME%\
echo.
echo 接下来：
echo   1. 将 %PROJECT_NAME% 文件夹压缩成 ZIP
echo   2. 复制到目标电脑
echo   3. 解压后双击 "环境配置.bat"
echo   4. 双击 "一键启动.bat" 启动系统
echo ================================================
echo.

set /p CREATE_ZIP=是否立即创建 ZIP 压缩包？(Y/N): 
if /i "%CREATE_ZIP%"=="Y" (
    echo.
    echo 正在创建压缩包...
    powershell -Command "Compress-Archive -Path '%EXPORT_DIR%\%PROJECT_NAME%\*' -DestinationPath '%EXPORT_DIR%\%PROJECT_NAME%.zip' -Force"
    echo.
    echo 压缩包已创建：%EXPORT_DIR%\%PROJECT_NAME%.zip
)

echo.
pause
