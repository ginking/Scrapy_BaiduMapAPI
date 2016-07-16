# coding:utf-8
from multiprocessing import Pool
import con_db
import xlrd
import os
from xlutils.copy import copy

import time


def get_uid():
    conn = con_db.get_connection()
    cursor = conn.cursor()
    sql = "select * from restaurants limit 0, 100"
    cursor.execute(sql)
    uid = set()
    data = cursor.fetchall()
    # 获得所有的uid
    for each_data in data:
        each_uid = each_data[2]
        uid.add(each_uid)
    conn.commit()
    cursor.close()
    conn.close()
    return uid


def deal_ktv():

    conn = con_db.get_connection()
    cursor = conn.cursor()
    wbk = xlrd.open_workbook(os.path.join(os.path.dirname(__file__), "data.xlsx"))
    rbk = copy(wbk)
    sheet = rbk.get_sheet(3)
    i = 1

    if i == 1:
        sql = "select * from restaurants limit 0, 100"
        cursor.execute(sql)
        uid = set()
        data = cursor.fetchall()
        # 获得所有的uid
        for each_data in data:
            each_uid = each_data[2]
            uid.add(each_uid)

    while len(uid):

        x_uid = uid.pop()
        query = "select * from restaurants where uid = '%s'" % x_uid
        cursor.execute(query)
        x_data = cursor.fetchall()
        distance = 2000
        closest_name = ""
        college_name = ""
        ktv_name = ""
        ktv_address = ""
        ktv_price = ""
        college_num = len(x_data)
        for xx_data in x_data:
            ktv_name = xx_data[1]
            ktv_address = xx_data[6]
            ktv_city = xx_data[7]
            ktv_province = xx_data[8]

            ktv_stars = xx_data[9]
            ktv_type = xx_data[10]

            college_name = xx_data[4] + "," + college_name
            ktv_price = xx_data[3]
            if int(xx_data[5]) <= distance:
                distance = int(xx_data[5])
                closest_name = xx_data[4]

        sheet.write(i, 0, ktv_name)
        sheet.write(i, 1, ktv_city)
        sheet.write(i, 2, ktv_province)
        sheet.write(i, 3, ktv_address)
        sheet.write(i, 4, ktv_price)
        sheet.write(i, 5, college_name)
        sheet.write(i, 6, college_num)
        sheet.write(i, 7, closest_name)
        sheet.write(i, 8, distance)
        sheet.write(i, 9, ktv_stars)
        sheet.write(i, 10, ktv_type)
        i += 1
        print i
    rbk.save(os.path.join(os.path.dirname(__file__), "data.xlsx"))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    deal_ktv()
    # print "parent process %s" % os.getpid()
    # p = Pool(9)
    # for i in range(5):
    #     p.apply_async(deal_ktv, args=(i,))
    # print "wait for all subprocess done"
    # p.close()
    # p.join()
    # print "all is done"