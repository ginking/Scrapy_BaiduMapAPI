# -*- coding: utf-8 -*-

import os
import con_db

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BaiduPipeline(object):
    def process_item(self, item, spider):
        return item


class KtvPipeline(object):

    def process_item(self, item, spider):
        conn = con_db.get_connection()
        cursor = conn.cursor()
        if self.__class__.__name__ in spider.pipelines:
            print "processing ktv"

            sql_1 = "SELECT `name`,city,province FROM `highschool` WHERE `position` = '%s'"
            cursor.execute(sql_1 % item['location'])
            data = cursor.fetchone()
            college = data[0]
            city = data[1]
            province = data[2]
            if city:
                pass
            else:
                city = ""
            if province:
                pass
            else:
                province = ""

            sql_2 = "insert into high_restaurants_2(`name`,uid,price,`college`,distance,address,city,province) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (item['name'], item['uid'], item['price'], college, item['distance'], item['address'], city, province)
            cursor.execute(sql_2, data)

            # sql = "select college,college_num,distance from restaurant where uid='%s'"
            # is_exist = cursor.execute(sql % item['uid'])
            # data1 = cursor.fetchone()

            # if is_exist:
            #     college1 = college + "-" + data1[0]
            #     num = int(data1[1]) + 1
            #
            #     if int(data1[2]) >= int(item['distance']):
            #         sql = "update restaurant set college = %s, college_num = %s,distance=%s,closest_college=%s where uid = %s"
            #         data = (college1, num, item['distance'], college, item['uid'])
            #     else:
            #         sql = "update restaurant set college = %s, college_num = %s where uid = %s"
            #         data = (college1, num, item['uid'])
            #     cursor.execute(sql, data)
            # else:
            #
            #     sql_2 = "insert into restaurant(`name`,uid,price,`college`,distance,closest_college,address,city,province,stars,`type`) " \
            #             "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #     data = (item['name'], item['uid'], item['price'], college, item['distance'], college, item['address'], city, province, item['overall_rating'], item['tag'])
            #     cursor.execute(sql_2, data)
            conn.commit()
            cursor.close()
            conn.close()
        else:
            return item
