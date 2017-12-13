# encoding: utf-8
'''
Created on 2017年12月11日

@author: dusaiya
'''
import numpy as np
import json

def loaduid(fpath, batchstr, batchtype,method_name):
    sets_a = "a"
    sets_b = "b"
    fin =open(fpath + "uid_city_result_"+method_name+"_" + batchtype + "_"  + batchstr ,"rb")
    filter_result=[]
    for line in fin.readlines():
        uid_pair=line.strip().split("\t")
        filter_result.append(uid_pair)
    fin.close()
    uidlist_a = np.loadtxt(fpath + 'uidlist_' + batchtype + "_" + batchstr + "_" + sets_a, dtype=np.str, delimiter="\t")
    uidlist_b = np.loadtxt(fpath + 'uidlist_' + batchtype + "_" + batchstr + "_" + sets_b, dtype=np.str, delimiter="\t")
    return filter_result,uidlist_a,uidlist_b

def getlabeluid(uidlist_a, uidlist_b):
    labellist = []
    for uid in uidlist_a:
        if uid in uidlist_b:
            labellist.append(uid)
    return labellist

def roundHandler_lower(fpath, batchstr, batchtype,kd_threshold,method_name):
    ## uid_bin_dict为查找字典
    filter_result,uidlist_a,uidlist_b = loaduid(fpath, batchstr, batchtype,method_name)
    correct_ct=0
    filter_ct=0
    for tmp_result in filter_result:
        if tmp_result[2]=="nan":
            continue
        if (kd_threshold<=float(tmp_result[2])):
            filter_ct+=1
            if tmp_result[0]==tmp_result[1]:
                correct_ct+=1
    label_list=getlabeluid(uidlist_a, uidlist_b)
    label_ct=len(label_list) ##符合的数据
    ## 筛选符合条件的结果集
    print str(float(correct_ct) / float(filter_ct)) +"\t"+str(float(correct_ct) / float(label_ct))+"\t"+str(filter_ct)

def roundHandler_uper(fpath, batchstr, batchtype,kd_threshold,method_name):
    ## uid_bin_dict为查找字典
    filter_result,uidlist_a,uidlist_b = loaduid(fpath, batchstr, batchtype,method_name)
    correct_ct=0
    filter_ct=0
    for tmp_result in filter_result:
        if tmp_result[2]=="nan":
            continue
        if (kd_threshold>=float(tmp_result[2])):
            filter_ct+=1
            if tmp_result[0]==tmp_result[1]:
                correct_ct+=1
    label_list=getlabeluid(uidlist_a, uidlist_b)
    label_ct=len(label_list) ##符合的数据
    ## 筛选符合条件的结果集
    print batchstr+"\t"+str(label_ct)+"\t"+str(float(correct_ct) / float(filter_ct)) +"\t"+str(float(correct_ct) / float(label_ct))+"\t"+str(filter_ct)+"\t"+str(int(float(correct_ct) / float(filter_ct) * float(filter_ct)))
    
if __name__ == '__main__':
    fpath = "./data2/"
    batchtype = "new"
    method_name=["kendalltau4city","hellinger_distance"]
    kd_threshold=0.25
    
    for batchno in range(0,5):
        batchstr=str(batchno)
        #roundHandler_lower(fpath, batchstr, batchtype,kd_threshold,method_name[1])
        roundHandler_uper(fpath, batchstr, batchtype,kd_threshold,method_name[1])
        
        