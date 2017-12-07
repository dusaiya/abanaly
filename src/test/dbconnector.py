# encoding: utf-8
'''
Created on 2017年11月15日

@author: alibaba


'''
import MySQLdb
from pymongo import MongoClient
import exceptions

def none_attr_value(dictValue,key):
    try:
        result=dictValue[key]
    except:
        result=""
    return result

def extract_tuple(weibo):
    try:
        date=weibo["ttl_time"]["date"]
        date=date.split(".")[0].replace("T"," ")
    except:
        date=None
    ip_addr=none_attr_value(weibo,"ip_addr")
    msg_province=none_attr_value(weibo,"msg_province").strip()
    msg_city=none_attr_value(weibo,"msg_city").strip()
    
    return (weibo["mid"],weibo["uid"],weibo["msg_type"],ip_addr,msg_province.encode("utf-8"),
            msg_city.encode("utf-8"),weibo["send_ip"],weibo["send_port"],weibo["insert_time"],weibo["real_time"],
            date,weibo["client_type"],weibo["net_type"],weibo["mobile_type"],weibo["client_remark"].encode("utf-8"))

def handler(mysqlconn, cur, weibodb, info):
    uid = info[0] #获取微博信息
    weibolist = list(weibodb.find({"uid":uid})) #信息抽取，产生list
    mysqllist=[]
    for weibo in weibolist:
        try:
            mysqlsql=extract_tuple(weibo) #输入微博dict
            mysqllist.append(mysqlsql)
        except exceptions.Exception,e:
            print "[ERROR]mid:"+weibo["mid"]+",msg:" +str(e)
        
    #根据list执行数据库insert
    #cur.execute("insert into m values (%s, %s )" , ("1","xiaoming"))
    cur.executemany("insert into weibo values (%s, %s, %s, %s, %s,\
                %s, %s, %s, %s, %s,\
                %s, %s, %s, %s, %s )", mysqllist)
    cur.execute("update weibo_id set flag=%s where uid=%s",("D",uid))
    mysqlconn.commit()
    
    
    
mysqlconn= MySQLdb.connect( host='10.60.1.73', port = 3306, user='shenhuawei',
         passwd='123456', db ='test2',charset="utf8")
cur = mysqlconn.cursor()
mongoconn=MongoClient("10.60.1.73",27017)
weibodb=mongoconn.weibo.content

uidct=cur.execute("select uid from weibo_id where weibo_ct>=10 and flag='T'")
infolist=cur.fetchmany(uidct)

ct=0
for info in infolist:
    handler(mysqlconn, cur, weibodb, info)
    ct+=1
    if ct%100==0:
        print ct



