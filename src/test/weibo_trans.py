# encoding: utf-8
'''
Created on 2017年11月9日

@author: dusaiya
'''
from pymongo import MongoClient
import json
import sys


if "__name__"=="__main__":
    if len(sys.argv)<2:
        batch_id="1"
    else:
        batch_id=sys.argv[1]    
    conn=MongoClient("10.60.1.73",27017)
    db2=conn.weibo.content
    
    fin=open("/data1/shenhuawei/msginfo-2016-6-"+batch_id+".json","rb")
    ct=0
    while(True):
        ct+=1
        s=fin.readline()
        dictob=json.loads(s.replace("$",""))
        db2.insert(dictob)
        if ct%1000==0:
            print ct
    fin.close()