# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class KtvItem(scrapy.Item):
    name = scrapy.Field()
    uid = scrapy.Field()
    location = scrapy.Field()
    address = scrapy.Field()
    page = scrapy.Field()
    distance = scrapy.Field()
    price = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    overall_rating = scrapy.Field()
    tag = scrapy.Field()
    num = scrapy.Field()
    nearby = scrapy.Field()

