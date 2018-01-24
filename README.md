# pyJAVBus

### Description:
`JAVBus` 爬虫项目练手项目,老司机专属


### Ajax抓取使用注意事项:
Python 使用 'scrapy-splash' 库
Docker 使用 `scrapinghub/splash`

### Warning:
**CentOS Only**
**Python3 Only**
1. 脚本中运行Docker与清除Swap功能仅在 `Centos` 系统下运用
2. 请在本地数据添加 `JavBusPython` 数据库
3. 数据库要求'UTF8'格式,可通过 `phpAdmin`添加,如果格式不对，日文无法插入

### USAGE:
1. 先安装Python依赖库 

```python
pip install -r require.txt
```
2.安装 Docker Image 

```c
docker pull scrapinghub/splash
```

~~3. 运行 Docker~~
(脚本集成了开启Docker功能 与 清除SwapMemory)功能

```c
docker run -p 8050:8050 scrapinghub/splash
```

4.运行爬虫

```python
python -m scrapy crawl JavbusSpider
```

### PS: 需要修改地方:
`pipelines.py` 中数据库信息
`JavbusSpider.py` 中爬取页面深度,默认第一第二页

### 关于部署(非必须,可手动开启脚本):

1. 使用 `scrapyd` 与 `scrapyd-client` , 已经包含在 `require.txt` 中

2. 开启 `Scrapyd` 服务

```c
scrapyd
```

或者后台开启

```c
nohup scrapyd > /dev/null 2>&1 &
```

开启后可通过 `http://localhost:6800` 访问

`如果部署在远程服务器，需要访问的话，需要修改Package下的config`

如:
使用 `pip` 安装 , 则在 `Python` 安装环境库下 `xxx(python库路径)/site-packages/scrapyd/default_scrapyd.conf`

修改 'bind_address = 0.0.0.0' , 然后开启防火墙规则,然后其他远侧会给你电脑能通过 `http://服务器ip:6800` 访问 `GUI` 控制台

3. 部署爬虫

进入项目, 修改 `scrapy.cfg` 中 `url`

命令行输入

```c
scrapyd-deploy [deploy_name]
```

进行部署,`deploy_name` 为 命令行 

```c
scrapyd-deploy -l
```

 中显示的名字

4. 运行爬虫

使用API
启动一个爬虫

```c
curl http://localhost:6800/schedule.json -d project=PROJECT_NAME -d spider=SPIDER_NAME
```

停止爬虫

```c
curl http://localhost:6800/cancel.json -d project=PROJECT_NAME -d job=JOB_ID
```

`project_name` 为爬虫`scrapy.cfg`项目名

`spider` 为项目中爬虫名字,[Spider文件夹下的]

6. 通过访问 `http://ip:6800` 观察爬虫情况




#### Last But Not Least

脚本只是提供提供爬取信息插入数据库收藏，此脚本不包括下载图片功能,如果需要下载图片数据,可运行

`python JAVBusImageDownloader.py`

下载数据库中所有信息中的图片,保存地址为文件夹根目录上一级目录，新建 `PYJavBus` 文件夹中


