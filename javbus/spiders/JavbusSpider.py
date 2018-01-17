# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from javbus.items import JavbusItem
from scrapy_splash import SplashRequest


class JavbusspiderSpider(scrapy.Spider):
    name = 'JavbusSpider'
    allowed_domains = ['www.javbus.cc']
    start_urls = ['https://www.javbus.cc/page/120']

    header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


    def start_requests(self):
        return [Request(self.start_urls[0],callback=self.parse,headers=self.header)]

    def parse(self, response):

        javList = response.xpath('//a[@class = "movie-box"]/@href').extract()
        for javItem in javList:
            # request =  Request(javItem,callback=self.parse_inner)
            request = SplashRequest(javItem, callback=self.parse_inner,args={'wait': 0.5})
            yield request
        for i in range(120,1,-1):
            page_url = 'https://www.javbus.cc/page/{}'.format(i)
            yield Request(page_url,callback=self.parse)


    def parse_inner(self,response):
        item = JavbusItem()
        #数组转字符
        #标题
        item['title'] = response.xpath('//div[@class = "container"]/h3/text()').extract()
        item['title'] = item['title'][0].replace('\t', "").replace('\n', "").replace(' ', "")
        #封面
        item['cover'] = response.xpath('//a[@class = "bigImage"]/@href').extract()
        item['cover'] = item['cover'][0]
        #番号
        item['code'] = response.xpath('//div[@class = "col-md-3 info"]/ p[1] / span[2]/text()').extract()
        item['code'] = item['code'][0]
        #发布日期
        item['date'] = response.xpath('//div[@class = "col-md-3 info"]/ p[2] / text()').extract()
        item['date'] = item['date'][0].replace('\t', "").replace('\n', "").replace(' ', "")
        #时长
        item['duration'] = response.xpath('//div[@class = "col-md-3 info"]/ p[3] /text()').extract()
        item['duration'] = item['duration'][0].replace('\t', "").replace('\n', "").replace(' ', "")
        #系列
        item['series'] = response.xpath('//span[@class = "genre"]/a/text()').extract()
        item['series'] = "||".join(item['series'])
        #类型
        item['type'] = response.xpath('//span[@class = "genre"]/a/text()').extract()
        item['type'] = "||".join(item['type'])
        #演员
        item['actress'] = response.xpath('//span[@class = "star-toggle"]/text()').extract()
        if item['actress'] is None or len(item['actress']) == 0:
            item['actress'] = ''
        else:
            item['actress'] = item['actress'][0]
        #封面图
        item['samplePic'] = response.xpath('//a[@class = "sample-box"]/@href').extract()
        item['samplePic'] = "||".join(item['samplePic'])
        #连接
        item['link'] = response.url
        #去重排序
        item['magnet'] = response.xpath('//table[@id = "magnet-table"]//tr//td/a/@href').extract()
        newMagnet = []
        for id in item['magnet']:
            if id not in newMagnet:
                newMagnet.append(id)
        item['magnet'] = "||".join(newMagnet)

        #去空格
        item['size'] =  response.xpath('//table[@id = "magnet-table"]//tr/td[2]/a/text()').extract()
        item['size'] = ("||".join(item['size'])).strip()
        item['size'] = item['size'].replace('\t',"").replace('\n',"").replace(' ',"")
        yield item