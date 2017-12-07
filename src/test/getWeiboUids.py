# encoding: utf-8
'''
Created on 2017年11月15日

@author: alibaba
'''
import MySQLdb
from pymongo import MongoClient
import datetime
starttime = datetime.datetime.now()
midtime=starttime
mysqlconn= MySQLdb.connect( host='10.60.1.73', port = 3306, user='shenhuawei',
         passwd='123456', db ='weibo', )
cur = mysqlconn.cursor()
mongoconn=MongoClient("10.60.1.73",27017)
weibodb=mongoconn.weibo.content

fin=open("./weiboUid.txt","rb")
weiboUids=fin.readlines()
print len(weiboUids)
flag="T"
ct=0
for uid in weiboUids:
    weibolist=list(weibodb.find({"uid":uid.strip()}))
    weibo_ct=len(weibolist)
    cur.execute("insert into abn_weibo_id values (%s, %s ,%s)" ,
                 (uid.strip(),flag,str(weibo_ct)))
    mysqlconn.commit()
    ct+=1
    if ct%100==0:
        endtime = datetime.datetime.now()
        print str(ct)+" uids have been done;total use \
 "+str((endtime - starttime).seconds) +" seconds; this 100 use\
 "+str((endtime - midtime).seconds) +" seconds."
        midtime=endtime
        
fin.close()
print "Done"