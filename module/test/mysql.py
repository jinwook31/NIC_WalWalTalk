#!/usr/bin/python
import pymysql
pymysql.install_as_MySQLdb()

import MySQLdb
db = MySQLdb.connect("118.42.88.117","root","qwer1234","NIC")

cur = db.cursor()

sql = "select sleep from module"
cur.execute(sql)

rows = cur.fetchall()
print(rows)

sql1 = "UPDATE module SET sleep=1"
cur.execute(sql1)

cur.execute(sql)
rows = cur.fetchall()
print(rows)

db.close()
