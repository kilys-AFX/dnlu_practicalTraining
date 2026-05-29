#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能零售分析系统 - 跨平台启动脚本
支持 Windows / macOS / Linux
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 版本过低，需要 3.8 或更高版本")
        print(f"   当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python 版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """检查依赖包"""
    required = [
        ("streamlit", "streamlit"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("plotly", "plotly"),
        ("sklearn", "scikit-learn"),
    ]
    
    missing = []
    for module, package in required:
        try:
            __import__(module)
            print(f"✓ {package} 已安装")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} 未安装")
    
    if missing:
        print(f"\n❌ 缺少依赖包: {', '.join(missing)}")
        return False
    return True

def install_dependencies():
    """安装依赖包"""
    print("\n正在安装依赖包...")
    requirements = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements):
        print("❌ 未找到 requirements.txt")
        return False
    
    try:
        # 使用清华镜像源加速
        cmd = [
            sys.executable, "-m", "pip", "install",
            "-r", requirements,
            "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
        ]
        subprocess.check_call(cmd)
        print("✓ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def create_directories():
    """创建必要目录"""
    dirs = ["data", "assets", "logs"]
    for d in dirs:
        path = os.path.join(os.path.dirname(__file__), d)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"✓ 创建目录: {d}")

def start_streamlit():
    """启动 Streamlit"""
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    
    if not os.path.exists(app_path):
        print(f"❌ 未找到主程序: {app_path}")
        return False
    
    print("\n" + "="*50)
    print("正在启动系统...")
    print("系统地址: http://localhost:8501")
    print("默认账号: admin")
    print("默认密码: admin123")
    print("="*50 + "\n")
    
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.port", "8501",
            "--server.address", "localhost"
        ]
        subprocess.run(cmd)
        return True
    except KeyboardInterrupt:
        print("\n\n系统已停止")
        return True
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

def main():
    """主函数"""
    print("="*50)
    print("智能零售用户行为分析系统 - 启动器")
    print("="*50)
    print()
    
    # 1. 检查 Python 版本
    print("[1/5] 检查 Python 版本...")
    if not check_python_version():
        input("\n按回车键退出...")
        sys.exit(1)
    
    # 2. 检查依赖
    print("\n[2/5] 检查依赖包...")
    if not check_dependencies():
        print("\n是否现在安装依赖包？(Y/N): ", end="")
        choice = input().strip().upper()
        if choice == "Y":
            if not install_dependencies():
                input("\n按回车键退出...")
                sys.exit(1)
        else:
            print("请手动运行: pip install -r requirements.txt")
            input("\n按回车键退出...")
            sys.exit(1)
    
    # 3. 创建目录
    print("\n[3/5] 创建必要目录...")
    create_directories()
    
    # 4. 提示信息
    print("\n[4/5] 准备启动...")
    print("- 系统地址: http://localhost:8501")
    print("- 默认账号: admin")
    print("- 默认密码: admin123")
    
    # 5. 启动系统
    print("\n[5/5] 启动系统...")
    start_streamlit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        input("\n按回车键退出...")
