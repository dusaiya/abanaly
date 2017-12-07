# encoding: utf-8
'''
Created on 2017年11月20日

@author: alibaba
'''
import MySQLdb
# import numpy as np
# import matplotlib.pyplot as plt
# 
# import random
mysqlconn = MySQLdb.connect(host='10.60.1.73', port=3306, user='shenhuawei',
         passwd='123456', db='test2', charset="utf8")
cur = mysqlconn.cursor()
uidct = cur.execute("select uid from weibo_id where weibo_ct>=100 and weibo_ct<500")
print str(uidct)
dts = cur.fetchmany(uidct)
mysqlconn.commit()
fout=open('./arealist_unique','wb')
areaset=[]
for dt in dts:
    temp_uid = dt[0]
    area_ct = cur.execute("select msg_city,count(1) from weibo where uid ='"
                        + temp_uid + 
        "' and msg_city<>'' and msg_city<>'" + 
        "白山".decode("utf8")
        + "' group by msg_city order by count(1) desc")
        
    arealist = cur.fetchmany(area_ct)
    mysqlconn.commit()
    if len(arealist) <= 1:
        continue
    else:
        fout.write(temp_uid+":")
        areastr=""
        for area in arealist:
            areastr+=area[0].encode("utf-8")
            areastr+=","
        if areastr not in areaset:
            areaset.append(areastr)
        fout.write(areastr+"\n")
print len(areaset)
fout.close()    
    
