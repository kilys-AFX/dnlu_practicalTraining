#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目导出脚本 - 自动打包项目为可分发版本
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_export_package():
    """创建导出包"""
    
    print("="*50)
    print("智能零售分析系统 - 项目导出")
    print("="*50)
    print()
    
    # 定义路径
    project_dir = Path(__file__).parent
    export_dir = project_dir / "export_package"
    package_name = "retail_analytics"
    package_dir = export_dir / package_name
    
    # 1. 创建导出目录
    print("[1/6] 创建导出目录...")
    if export_dir.exists():
        shutil.rmtree(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. 定义要复制的文件和目录
    print("[2/6] 复制核心文件...")
    
    # 核心文件
    core_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "部署说明.md",
        "快速部署指南.md",
        "一键启动.bat",
        "环境配置.bat",
        "start.py",
        "start_mac_linux.sh",
        "verify_installation.py",
        "导出清单.txt",
        "导出指南.txt",
        "部署总结.md",
        "CHECK_DEPENDENCIES.md",
    ]
    
    for file in core_files:
        src = project_dir / file
        if src.exists():
            shutil.copy2(src, package_dir)
            print(f"  [OK] {file}")
        else:
            print(f"  [MISSING] 未找到: {file}")
    
    # 3. 复制目录
    print("\n[3/6] 复制代码目录...")
    
    dirs_to_copy = [
        "config",
        "data",
        "pages",
        "utils",
        "models",
        "assets",
        "deploy",
    ]
    
    for dir_name in dirs_to_copy:
        src = project_dir / dir_name
        dst = package_dir / dir_name
        
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                "*.pyc",
                "__pycache__",
                "*.db",
                "*.log",
                "*.sqlite",
            ))
            print(f"  [OK] {dir_name}/")
        else:
            print(f"  [MISSING] 未找到: {dir_name}/")
    
    # 4. 清理临时文件
    print("\n[4/6] 清理临时文件...")
    clean_temp_files(package_dir)
    
    # 5. 创建快速开始指南
    print("\n[5/6] 创建快速开始指南...")
    create_quick_start_guide(package_dir)
    
    # 6. 创建 ZIP 压缩包
    print("\n[6/6] 创建 ZIP 压缩包...")
    zip_path = export_dir / f"{package_name}.zip"
    
    try:
        create_zip_package(package_dir, zip_path)
        print(f"  ✓ 压缩包已创建: {zip_path}")
    except Exception as e:
        print(f"  ✗ 创建压缩包失败: {e}")
    
    # 完成
    print("\n" + "="*50)
    print("导出完成！")
    print("="*50)
    print()
    print(f"导出位置：{package_dir}")
    print()
    print("接下来：")
    print("  1. 将 retail_analytics 文件夹压缩成 ZIP")
    print("  2. 复制到目标电脑")
    print("  3. 解压后双击 '环境配置.bat'")
    print("  4. 双击 '一键启动.bat' 启动系统")
    print()
    
    return True

def clean_temp_files(directory):
    """清理临时文件"""
    # 删除 .pyc 文件
    for pyc_file in directory.rglob("*.pyc"):
        pyc_file.unlink()
        print(f"  [OK] 删除: {pyc_file.relative_to(directory)}")
    
    # 删除 __pycache__ 目录
    for cache_dir in directory.rglob("__pycache__"):
        shutil.rmtree(cache_dir)
        print(f"  [OK] 删除: {cache_dir.relative_to(directory)}/")
    
    # 删除 .db 文件
    for db_file in directory.rglob("*.db"):
        db_file.unlink()
        print(f"  [OK] 删除: {db_file.relative_to(directory)}")
    
    # 删除 .log 文件
    for log_file in directory.rglob("*.log"):
        log_file.unlink()
        print(f"  [OK] 删除: {log_file.relative_to(directory)}")

def create_zip_package(source_dir, zip_path):
    """创建 ZIP 压缩包"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(source_dir.parent)
                zipf.write(file_path, arcname)

def create_quick_start_guide(directory):
    """创建快速开始指南"""
    guide_path = directory / "快速开始.txt"
    
    content = """================================================
        智能零售分析系统 - 快速开始
================================================

【3步快速部署】

第 1 步：安装 Python
  1. 访问 https://www.python.org/downloads/
  2. 下载 Python 3.8 或更高版本
  3. 安装时务必勾选 "Add Python to PATH"
  4. 验证：打开 CMD，输入 python --version

第 2 步：配置环境
  1. 解压本项目到任意目录
  2. 双击运行 "环境配置.bat"
  3. 等待依赖安装完成（约 2-5 分钟）

第 3 步：启动系统
  1. 双击运行 "一键启动.bat"
  2. 等待系统启动（首次约 1-2 分钟）
  3. 浏览器打开 http://localhost:8501
  4. 登录：admin / admin123

【常见问题】

Q: Python 安装后提示"不是内部或外部命令"
A: 重新安装 Python，勾选 "Add Python to PATH"，或重启电脑

Q: 依赖安装失败
A: 右键"环境配置.bat"，选择"以管理员身份运行"

Q: 端口被占用
A: 编辑"一键启动.bat"，将 8501 改为 8502

【详细文档】

- 快速部署指南.md    (3步快速开始)
- 部署说明.md         (完整部署文档)
- 导出指南.txt        (完整导出说明)
- CHECK_DEPENDENCIES.md (依赖检查清单)

【系统要求】

- Python 3.8+
- 内存 4GB 以上
- 磁盘 500MB 可用空间

【默认账号】

账号：admin
密码：admin123

⚠️ 生产环境请务必修改默认密码！

================================================
            祝使用愉快！
================================================
"""
    
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  ✓ 创建: 快速开始.txt")

if __name__ == "__main__":
    try:
        create_export_package()
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"\n[ERROR] Export failed: {e}")
        input("\nPress Enter to exit...")
