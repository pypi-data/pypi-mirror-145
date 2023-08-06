# 使用 pipreqs 处理依赖
### 安装
```
pip install pipreqs
```

### 在当前目录生成
```
pipreqs . --encoding=utf8 --force
```

### 使用requirements.txt安装依赖的方式
```
pip install -r requirements.txt
```

### 打包成wheel
先安装最新的setuptools和wheel
```
python3 -m pip install --user --upgrade setuptools wheel
```
再执行打包命令
```
python3 setup.py sdist bdist_wheel
```