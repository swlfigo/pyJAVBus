# pyJAVBus

### Ajax抓取使用注意事项:
Python 使用 'scrapy-splash' 库
Docker 使用 `scrapinghub/splash`

### USAGE:
1. 先安装Python依赖库 

```python
pip install -r require.txt
```
2.安装 Docker Image 

```c
docker pull scrapinghub/splash
```

3. 运行 Docker

```c
docker run -p 8050:8050 scrapinghub/splash
```

4.运行爬虫

```python
python -m scrapy crawl JavbusSpider
```

