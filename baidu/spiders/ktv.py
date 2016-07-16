# -*- coding: utf-8 -*-
import scrapy
from baidu.items import KtvItem
import baidu.con_db
import json

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class KtvSpider(scrapy.Spider):
    name = "ktv"
    pipelines = ['KtvPipeline']

    start_urls = (
        'http://www.baidu.com/',
    )

    i = 0

    def parse(self, response):
        data = baidu.con_db.get_position()
        positions = data['positions']

        for position in positions:
            item = KtvItem()
            item['location'] = position
            item['page'] = 0
            response.meta['item'] = item
            print str(item['page'])
            print position
            url = "http://api.map.baidu.com/place/v2/search?query=餐馆&location=" + position + \
                  "&radius=1000&output=json&ak=x5OeNcNKGL38tHahnq2xKxn4loTPKQVO&page_size=20&scope=2&page_num=" + str(item['page'])
            yield scrapy.Request(url=url, callback=self.parse_ktv, meta=response.meta)

    def parse_ktv(self, response):
        data = json.loads(response.body)
        results = data['results']
        item = response.meta['item']
        if len(results) != 0:
            for each in results:
                item['name'] = each['name']
                item['uid'] = each['uid']
                item['address'] = each['address']
                item['distance'] = each['detail_info']['distance']
                if 'price' in each['detail_info']:
                    item['price'] = each['detail_info']['price']
                else:
                    item['price'] = ""
                # # 餐馆额外的数据
                # if 'overall_rating' in each['detail_info']:
                #     item['overall_rating'] = each['detail_info']['overall_rating']
                # else:
                #     item['overall_rating'] = ""
                # if 'tag' in each['detail_info']:
                #     item['tag'] = each['detail_info']['tag']
                # else:
                #     item['tag'] = ""

                yield item

        if len(results) == 20:
            item['page'] += 1
            response.meta['item'] = item
            url = "http://api.map.baidu.com/place/v2/search?query=餐馆&location=" + item['location'] + \
                  "&radius=1000&output=json&ak=x5OeNcNKGL38tHahnq2xKxn4loTPKQVO&page_size=20&scope=2&page_num=" + str(item['page'])
            yield scrapy.Request(url=url, callback=self.parse_ktv, meta=response.meta)
