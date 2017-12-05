# encoding: utf-8
'''
Created on 2017年11月18日

@author: alibaba
'''
import MySQLdb
mysqlconn= MySQLdb.connect( host='10.60.1.73', port = 3306, user='shenhuawei',
         passwd='123456', db ='test2',charset="utf8")
cur = mysqlconn.cursor()
cur.execute("insert into m values (%s,%s)" ,(2,"北京"))
mysqlconn.commit()