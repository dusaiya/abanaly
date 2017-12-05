# encoding: utf-8
'''
Created on 2017年11月14日

@author: dusaiya
'''
import MySQLdb
conn= MySQLdb.connect(
        host='10.60.1.73',
        port = 3306,
        user='shenhuawei',
        passwd='123456',
        db ='test',
        )
cur = conn.cursor()

