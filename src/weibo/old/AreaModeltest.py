# encoding: utf-8
'''
Created on 2017年11月28日

@author: alibaba
'''
import MySQLdb
import random

def dbInfo():
    conn = MySQLdb.connect(host='10.60.1.73', port=3306, user='shenhuawei',
             passwd='123456', db='test2', charset="utf8")
    cur = conn.cursor()
    return conn, cur

def get_uidlist(conn,cur):  
    uidct = cur.execute("select uid from uid_city_over_3")
    dts = cur.fetchmany(uidct)
    conn.commit()
    uidlist=[]
    for dt in dts:
        uidlist.append(str(dt[0]))
    return uidlist

def get_weibolist(uid,conn,cur,preDay,sufDay):
    '''
    自动获取80%的数据
    '''
    weiboct = cur.execute("select msg_city from weibo where uid=%s "+" and msg_city<>'' and msg_city<>'" + 
        "白山".decode("utf8") + "' and real_date>=%s and real_date<%s",
                          (uid,preDay,sufDay))
    dts = cur.fetchmany(weiboct)
    conn.commit()
    tmp_list=[]
    for dt in dts:
        tmp_list.append(str(dt[0].encode("utf-8")))
    return random.sample(tmp_list,len(tmp_list)*8/10),uid
    #return tmp_list,uid

def uid_extract_save(uidlist,ct,filestr):
    new_uidlist=random.sample(uidlist,ct)
    fout=open("./data/uidlist_"+filestr,"wb")
    for uid in new_uidlist:
        fout.write(uid)
        fout.write("\n")
    fout.close()
    return new_uidlist

def weibo_get_save(uidlist, conn, cur, preDay, sufDay,filestr):
    print "length of uidlist_"+ filestr+":"+ str(len(uidlist_a))
    i=0
    fout=open("./data/weibolist_"+filestr,"wb")
    for uid in uidlist:
        weibolist,uid=get_weibolist(uid, conn, cur, preDay, sufDay)
        for weibo in weibolist:
            fout.write(uid+"\t"+weibo+"\n")
            i+=1
            if i%10000==0:
                print i
    fout.close()
    print "length of weibolist_"+ filestr+":"+ str(i)

if __name__ == "__main__":
    conn,cur=dbInfo()
    uidlist=get_uidlist(conn,cur)
    batchstr="3"
    batchtype="half"
    seta="a"
    setb="b"
    
    uidlist_a=uid_extract_save(uidlist,2500,batchtype+"_"+seta+"_"+batchstr) # 2500 大约 75%
    uidlist_b=uid_extract_save(uidlist,2500,batchtype+"_"+setb+"_"+batchstr) 
    preDay="2016-06-01"
    sufDay="2016-06-16"
    weibo_get_save(uidlist_a, conn, cur, preDay, sufDay,batchtype+"_"+seta+"_"+batchstr)
    preDay="2016-06-01"
    sufDay="2016-06-16"
    weibo_get_save(uidlist_b, conn, cur, preDay, sufDay,batchtype+"_"+setb+"_"+batchstr)
    
    