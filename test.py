import MySQLdb

conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='macwaning',
        db ='college',
        charset='utf8'
        )
cur = conn.cursor()

cur.execute("select * from kalist where subchannel like '%QSR%' and isnull(str)")
results = cur.fetchall()
for row in results:
    print row[4]
    id = row[0]
    tradernames = row[4]
    str = row[5]
    cur.execute('update kalist set str = %s where id=%s',(tradernames,id))
    conn.commit()

cur.close()
conn.commit()
conn.close()
