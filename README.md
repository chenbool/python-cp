# python-cp

Python 彩票开奖信息抓取工具，支持多种彩票类型数据采集。

## 项目简介

本项目用于抓取彩票开奖信息，包括双色球、大乐透、福彩3D、体彩排列三等多种彩票类型。数据来源为开源彩票开奖平台。

## 技术栈

| 分类 | 技术 |
|------|------|
| 编程语言 | Python 3.x |
| HTTP 客户端 | requests |
| 并发处理 | gevent |
| HTML 解析 | lxml |
| 数据库 | SQLite |

## 项目结构

```
python-cp/
├── cp.py                    # 彩票数据抓取主程序
├── db.py                    # 数据库操作
├── hb.py                   # 红包/活动相关
├── data.db                 # SQLite 数据文件
├── data.sql                # 数据表结构
├── kan.sql                 # 开奖数据
├── main.sql                # 主数据
├── requirements.txt        # 项目依赖
├── demo.gif                # 演示动画
├── kan84/                  # 副本抓取模块
│   ├── app.py             # 应用主程序
│   ├── app1.py            # 应用备份
│   └── requirements.txt   # 依赖
├── manhua/                # 漫画抓取模块
│   ├── app.py            # 抓取程序
│   └── requirements.txt  # 依赖
├── pythhon3/             # Python3 漫画抓取
│   ├── z_mankezhan.py   # 漫画栈抓取
│   ├── z_lieqi.py       # 猎奇漫画抓取
│   ├── v.py             # 通用抓取工具
│   └── requirements.txt # 依赖
└── mysqlclient/          # MySQL 客户端 Windows wheel 文件
```

## 核心模块

### cp.py - 彩票数据抓取

```python
class Train(object):
    baseUrl = 'https://kjh.55128.cn'
    
    def run(self):
        # 获取彩票开奖信息
        tree = self.get_content('/k/index.html')
        # 处理数据...
```

### db.py - 数据库操作

负责 SQLite 数据库的创建、读写操作。

### hb.py - 活动相关

处理红包、活动相关数据。

## 安装依赖

```bash
pip install -r requirements.txt
```

或者使用 pipreqs 自动生成依赖：

```bash
pipreqs ./ --encoding=utf8
```

## 依赖说明

| 包名 | 版本 | 说明 |
|------|------|------|
| requests | 2.18.4 | HTTP 客户端 |
| gevent | - | 协程并发 |
| lxml | - | HTML/XML 解析 |

## mysqlclient 安装

Windows 环境需要安装 Visual C++ 编译工具，建议使用预编译的 wheel 文件：

```bash
pip install mysqlclient-1.4.2-cp37-cp37m-win_amd64.whl
```

下载地址：https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

## 使用方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行主程序
python cp.py

# 运行漫画抓取
python manhua/app.py

# 运行副本抓取
python kan84/app.py
```

## 数据库说明

项目使用 SQLite 存储数据，主要数据表：

- `data.db` - 主数据库文件
- `kan.sql` - 开奖记录表结构
- `main.sql` - 主数据表结构

## 相关链接

- [mysqlclient Windows 安装包](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)

## 许可证

MIT License
