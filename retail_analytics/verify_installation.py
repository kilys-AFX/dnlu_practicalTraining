#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装验证脚本 - 检查系统是否可以正常运行
"""

import sys
import os

def check_python():
    """检查 Python 版本"""
    print("检查 Python 版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"  ✗ Python 版本过低: {version.major}.{version.minor}")
        return False
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_package(module_name, package_name=None):
    """检查单个包是否安装"""
    if package_name is None:
        package_name = module_name
    try:
        __import__(module_name)
        return True
    except ImportError:
        print(f"  ✗ 未安装: {package_name}")
        return False

def check_dependencies():
    """检查所有依赖"""
    print("\n检查依赖包...")
    
    packages = [
        ("streamlit", "streamlit"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("plotly", "plotly"),
        ("sklearn", "scikit-learn"),
        ("requests", "requests"),
        ("openpyxl", "openpyxl"),
    ]
    
    all_installed = True
    for module, package in packages:
        if check_package(module, package):
            print(f"  ✓ {package}")
        else:
            all_installed = False
    
    return all_installed

def check_files():
    """检查必需文件是否存在"""
    print("\n检查项目文件...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "config/settings.py",
        "data/database.py",
        "data/data_generator.py",
        "pages/data_management.py",
        "pages/data_overview.py",
        "pages/behavior_analysis.py",
        "pages/user_profiling.py",
        "pages/ai_assistant.py",
        "utils/data_processor.py",
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ 缺失: {file}")
            all_exist = False
    
    return all_exist

def check_directories():
    """检查必需目录是否存在"""
    print("\n检查项目目录...")
    
    required_dirs = [
        "config",
        "data",
        "pages",
        "utils",
        "models",
        "assets",
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ 缺失: {dir_name}/")
            all_exist = False
    
    return all_exist

def test_import():
    """测试主程序导入"""
    print("\n测试主程序导入...")
    
    try:
        # 测试各模块导入
        from data.database import init_database
        print("  ✓ data.database")
        
        from data.data_generator import generate_all_data
        print("  ✓ data.data_generator")
        
        from utils.data_processor import clean_data, calculate_rfm
        print("  ✓ utils.data_processor")
        
        return True
    except ImportError as e:
        print(f"  ✗ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False

def main():
    """主函数"""
    print("="*50)
    print("智能零售分析系统 - 安装验证")
    print("="*50)
    
    checks = []
    
    # 1. 检查 Python
    checks.append(("Python 版本", check_python()))
    
    # 2. 检查依赖
    checks.append(("依赖包", check_dependencies()))
    
    # 3. 检查文件
    checks.append(("项目文件", check_files()))
    
    # 4. 检查目录
    checks.append(("项目目录", check_directories()))
    
    # 5. 测试导入
    checks.append(("模块导入", test_import()))
    
    # 汇总结果
    print("\n" + "="*50)
    print("验证结果汇总")
    print("="*50)
    
    all_passed = True
    for name, result in checks:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("✓ 所有检查通过！系统可以正常启动")
        print("\n启动命令：")
        print("  Windows: 双击 '一键启动.bat'")
        print("  手动:    streamlit run app.py")
    else:
        print("✗ 部分检查未通过，请查看上述错误信息")
        print("\n建议操作：")
        print("  1. 双击运行 '环境配置.bat' 安装依赖")
        print("  2. 检查项目文件是否完整")
        print("  3. 查看 '部署说明.md' 获取帮助")
    print("="*50)
    
    input("\n按回车键退出...")
    return all_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n验证已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 验证过程出错: {e}")
        input("\n按回车键退出...")
        sys.exit(1)
