# encoding: utf-8
'''
Created on 2017年11月18日
制作，微博分布的图片
@author: alibaba

'''
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt

import random

def weibo_ct_distribution(mysqlconn, cur):
    uidct = cur.execute("select uid, weibo_ct from weibo_id")
    #uidct = cur.execute("select uid, weibo_ct from weibo_id where flag='D'")
    dts = cur.fetchmany(uidct)
    dataSets = []
    fout = open("./weibo_ct_distribution", "wb")
    for dt in dts:
        fout.write(dt[0] + "," + str(dt[1]) + "\n")
        dataSets.append(int(dt[1]))

    fout.close()
    mysqlconn.commit()
    plotDataset = [[], []]
    fig = plt.figure()  
    ax=fig.add_subplot(111)
    ax.hist(np.array(dataSets), 1500, log=True)
    #ax.semilogx()
    plt.xlabel('weibo counts')
    plt.xlim(0.0, 2000)
    plt.ylabel('Frequency')
    plt.title('weibo counts Frequency (2016-6)') 
    #plt.show()
    plt.savefig('./weibo_ct_distribution_1.jpg')
    #plt.savefig('./weibo_ct_distribution_2.jpg'
    
def sampleUserFrequency_24(mysqlconn, cur, a,b,ct):
    uidct = cur.execute("select uid from weibo_id where weibo_ct>=%s\
     and weibo_ct<%s",(a,b))
    dts = cur.fetchmany(uidct)
    uidlist=random.sample(dts,ct)
    mysqlconn.commit()
    fig = plt.figure()
    for i in range(ct):
        ax=fig.add_subplot(2,2,i+1)
        temp_uid=uidlist[i][0]
        weiboct = cur.execute("select substr(real_date,12,2) from weibo where uid="+temp_uid)
        dts = cur.fetchmany(weiboct)
        dataSets = []
        for dt in dts:
            dataSets.append(int(dt[0]))
        ax.hist(np.array(dataSets), bins=24,range=(0,23))
        plt.xlabel('hour')
        plt.xlim(0, 23)
        #ax.set_xticks(np.linspace(0,24,9)) 
        #ax.set_xticklabels( (0, 2,4,6,8,10,12,14,16,18,20,22))
        plt.ylabel('count')
        plt.title('uid:'+temp_uid)
        plt.subplots_adjust(hspace=0.26)
    plt.suptitle(">"+str(a)+";<"+str(b));
    plt.show()
    
def sampleUserFrequency_6(mysqlconn, cur, a,b,ct):
    uidct = cur.execute("select uid from weibo_id where weibo_ct>=%s\
     and weibo_ct<%s",(a,b))
    dts = cur.fetchmany(uidct)
    uidlist=random.sample(dts,ct)
    mysqlconn.commit()
    fig = plt.figure()
    for i in range(ct):
        ax=fig.add_subplot(2,2,i+1)
        temp_uid=uidlist[i][0]
        weiboct = cur.execute("select cast(substr(real_date,12,2) as signed)/4 from weibo where uid="+temp_uid)
        dts = cur.fetchmany(weiboct)
        dataSets = []
        for dt in dts:
            dataSets.append(int(dt[0]))
        ax.hist(np.array(dataSets), bins=6,range=(0,6))
        plt.xlabel('hour')
        plt.xlim(0, 6)
        ax.set_xticks(np.linspace(0.5,5.5,6)) 
        ax.set_xticklabels( ('0-3','4-7','8-11','12-15','16-19','20-23'))
        plt.ylabel('count')
        plt.title('uid:'+temp_uid)
        plt.subplots_adjust(hspace=0.26)
    plt.suptitle(">"+str(a)+";<"+str(b));
    plt.show()
def uidweekFrequency(uid,timelist):
    ct=len(timelist)-1
    fig = plt.figure()
    for i in range(ct):
        ax=fig.add_subplot(2,4,i+1)
        preDay=timelist[i]
        sufDay=timelist[i+1]
        weiboct = cur.execute("select substr(real_date,12,2) from weibo where uid=%s and real_date>=%s and real_date<%s",
                              (uid,preDay,sufDay))
        dts = cur.fetchmany(weiboct)
        dataSets = []
        for dt in dts:
            dataSets.append(int(dt[0]))
        ax.hist(np.array(dataSets), bins=24,range=(0,23))
        plt.xlabel('hour')
        plt.xlim(0, 23)
        plt.ylim(0, 10)
        #ax.set_xticks(np.linspace(0,24,9)) 
        #ax.set_xticklabels( (0, 2,4,6,8,10,12,14,16,18,20,22))
        plt.ylabel('count')
        plt.title('date:'+preDay)
        plt.subplots_adjust(hspace=0.26)
    mysqlconn.commit()
    plt.suptitle("uid:"+uid);
    plt.show()
def uidweekFrequency_6(uid,timelist):
    ct=len(timelist)-1
    fig = plt.figure()
    for i in range(ct):
        ax=fig.add_subplot(2,4,i+1)
        preDay=timelist[i]
        sufDay=timelist[i+1]
        weiboct = cur.execute("select cast(substr(real_date,12,2) as signed)/4 from weibo where uid=%s and real_date>=%s and real_date<%s",
                              (uid,preDay,sufDay))
        dts = cur.fetchmany(weiboct)
        dataSets = []
        for dt in dts:
            dataSets.append(int(dt[0]))
        ax.hist(np.array(dataSets), bins=6,range=(0,6))
        plt.xlabel('hour')
        plt.xlim(0, 6)
        plt.ylim(0, 40)
        ax.set_xticks(np.linspace(0.5,5.5,6)) 
        ax.set_xticklabels( ('0-3','4-7','8-11','12-15','16-19','20-23'))
        plt.ylabel('count')
        plt.title('date:'+preDay)
        plt.subplots_adjust(hspace=0.26)
    mysqlconn.commit()
    plt.suptitle("uid:"+uid);
    plt.show()
    
mysqlconn= MySQLdb.connect( host='10.60.1.73', port = 3306, user='shenhuawei',
         passwd='123456', db ='test2',charset="utf8")
cur = mysqlconn.cursor()

#weibo_ct_distribution(mysqlconn, cur) 
#sampleUserFrequency_24(mysqlconn, cur, 10,30,int(4))
#sampleUserFrequency_6(mysqlconn, cur, 100,500,int(4))

timelist1=["2016-06-05","2016-06-06","2016-06-07","2016-06-08",
           "2016-06-09","2016-06-10","2016-06-11","2016-06-12","2016-06-13"]
timelist2=["2016-06-12","2016-06-13","2016-06-14","2016-06-15",
           "2016-06-16","2016-06-17","2016-06-18","2016-06-19","2016-06-20"]
timelist3=["2016-06-19","2016-06-20","2016-06-21","2016-06-22",
           "2016-06-23","2016-06-24","2016-06-25","2016-06-26","2016-06-27"]
uid="1802267337"
#uid="1921880637"
uidweekFrequency_6(uid,timelist1)
uidweekFrequency_6(uid,timelist2)
uidweekFrequency_6(uid,timelist3)
