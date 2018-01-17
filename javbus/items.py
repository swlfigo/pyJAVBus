# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JavbusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
    code = scrapy.Field()
    date = scrapy.Field()
    duration = scrapy.Field()
    series = scrapy.Field()
    type = scrapy.Field()
    actress = scrapy.Field()
    magnet = scrapy.Field()
    size = scrapy.Field()
    samplePic = scrapy.Field()
    link = scrapy.Field()


class JavBusImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()