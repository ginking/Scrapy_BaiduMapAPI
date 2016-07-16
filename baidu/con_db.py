import MySQLdb
import xlrd
import os
import urllib


def get_connection():
    # conn = MySQLdb.connect(host="localhost", user="root", passwd="067116", db="baidu", charset="utf8")
    conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='macwaning',
        db ='college',
        charset='utf8'
        )
    return conn


def import_data():
    conn = get_connection()
    cursor = conn.cursor()

    wbk = xlrd.open_workbook(os.path.join(os.path.dirname(__file__), "high.xlsx"))
    table = wbk.sheet_by_index(0)
    row_num = table.nrows

    for i in range(0, row_num):
        sql = "insert into highschool(`name`,address,`position`) " \
              "values(%s,%s,%s)"
        table_data = table.row_values(i)
        print table_data[1]
        data = (table_data[1], table_data[2], table_data[3])
        cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()


def get_position():
    positions = list()
    names = list()

    conn = get_connection()

    cursor = conn.cursor()
    sql = 'select `position`,`name` from highschool'
    cursor.execute(sql)
    for req in cursor.fetchall():
        if req[0]:
            positions.append(req[0])
            names.append(req[1])
    conn.commit()
    cursor.close()
    conn.close()
    # print positions
    return {'positions': positions, 'names': names}

def get_highscool():
    conn = get_connection()

    cursor = conn.cursor()
    sql = 'select `college`,`name` from chaoshi1'
    cursor.execute(sql)
    l = set()
    for req in cursor.fetchall():
        if req[0]:
            n = req[0]
            l.add(n)
    print len(l)

def deal_data():
    conn = get_connection()
    cursor = conn.cursor()
    sql = 'select `name`,city,province,url from highschoolNew'
    cursor.execute(sql)
    for req in cursor.fetchall():
        name = req[0]
        city = req[1]
        province = req[2]
        url = req[3]
        sql = 'insert into highschool(`name`,city,province,url) values(%s,%s,%s,%s)'
        data = (name, city, province, url)
        cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

def get_name():
    conn = get_connection()
    cursor = conn.cursor()
    sql = 'select `name`,city,province from highschool'
    cursor.execute(sql)
    urls = list()
    for req in cursor.fetchall():
        url = "http://api.map.baidu.com/place/v2/search?q=" + urllib.quote_plus(str(req[0]).strip()) + \
              "&region=" + urllib.quote_plus((str(req[2]))) + \
              "&page_size=5&page_num=0&output=json&ak=x5OeNcNKGL38tHahnq2xKxn4loTPKQVO"
        urls.append(url)
        print url

    conn.commit()
    cursor.close()
    conn.close()
    return urls

def test():
    conn = get_connection()
    cursor = conn.cursor()
    sql = 'select chaoshi_1000 from junior'
    cursor.execute(sql)
    num = 0
    for req in cursor.fetchall():
        print req[0]
        num += int(req[0])
    print num
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    test()
