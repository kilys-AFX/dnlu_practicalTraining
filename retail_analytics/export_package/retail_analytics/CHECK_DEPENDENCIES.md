# 依赖检查清单

## Python 环境

- [ ] Python 3.8+ 已安装
- [ ] pip 可用
- [ ] Python 已添加到 PATH

**检查命令**：
```bash
python --version
pip --version
```

## 必需依赖包

### 核心框架
- [ ] streamlit >= 1.30.0
- [ ] streamlit-antd-components >= 0.2.0
- [ ] streamlit-autorefresh >= 0.0.4

### 数据处理
- [ ] pandas >= 2.0.0
- [ ] numpy >= 1.24.0

### 数据可视化
- [ ] plotly >= 5.15.0

### 机器学习
- [ ] scikit-learn >= 1.3.0

### 深度学习（可选）
- [ ] torch >= 2.0.0
- [ ] torchvision >= 0.15.0

### API 调用
- [ ] requests >= 2.31.0
- [ ] openai >= 1.0.0

### Excel 处理
- [ ] openpyxl >= 3.1.0
- [ ] xlrd >= 2.0.0

### 其他工具
- [ ] python-dateutil >= 2.8.0
- [ ] pytz >= 2023.3
- [ ] PyYAML >= 6.0.0
- [ ] toml >= 0.10.2
- [ ] psutil >= 5.9.0

## 检查命令

### 批量检查
```bash
pip list | findstr -i "streamlit pandas numpy plotly sklearn torch requests openai openpyxl"
```

### 单独检查
```bash
python -c "import streamlit; print(streamlit.__version__)"
python -c "import pandas; print(pandas.__version__)"
python -c "import numpy; print(numpy.__version__)"
python -c "import plotly; print(plotly.__version__)"
python -c "import sklearn; print(sklearn.__version__)"
```

## 安装命令

### 使用 requirements.txt（推荐）
```bash
pip install -r requirements.txt
```

### 使用国内镜像源（加速）
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 手动安装核心包
```bash
pip install streamlit pandas numpy plotly scikit-learn
```

## 常见问题

### 1. pip 不是内部或外部命令
**原因**：Python 未添加到 PATH

**方案**：
- 重新安装 Python，勾选 "Add Python to PATH"
- 或手动添加 Python 安装目录到环境变量

### 2. 安装速度慢
**原因**：默认使用国外源

**方案**：使用国内镜像源
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 权限错误
**原因**：无管理员权限

**方案**：
```bash
pip install --user -r requirements.txt
```

### 4. 版本冲突
**原因**：已安装的包版本不兼容

**方案**：
```bash
pip install --upgrade -r requirements.txt
```

## 验证安装

运行以下命令，全部通过则说明环境正常：

```bash
python -c "import streamlit, pandas, numpy, plotly, sklearn; print('✓ 所有核心依赖安装成功')"
```

如果输出成功信息，则可以启动系统：

```bash
streamlit run app.py
```
