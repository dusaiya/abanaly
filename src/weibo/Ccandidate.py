# encoding: utf-8
'''
Created on 2017年11月30日

@author: alibaba



'''
import numpy as np

def loaddata(fpath, batchstr, batchtype, sets):
    uidlist = np.loadtxt(fpath + 'uidlist_' + batchtype + "_" + sets + "_" + batchstr, dtype=np.str, delimiter="\t")
    uidcity_list = np.loadtxt(fpath + 'uid_city_common_' + batchtype + "_" + sets + "_" + batchstr, dtype=np.str, delimiter="\t")
    return uidlist, uidcity_list

def getlabeluid(uidlist_a, uidlist_b):
    labellist = []
    for uid in uidlist_a:
        if uid in uidlist_b:
            labellist.append(uid)
    return labellist

def getresult(uidcity_list_a, uidcity_list_b):
    fp_ct = 0  # False Positive 的数量 
    tp_uid_list = []
    
    for uidcit in uidcity_list_a:
        ts=np.where(uidcity_list_b==uidcit[1])
        lts=uidcity_list_b[ts[0],:]
        for lt in lts:
            if str(lt[0])==str(uidcit[0]):
                tp_uid_list.append(str(lt[0]))
#                 print "b file:"+str(lt[0]) +";a file:"+ str(uidcit[0])
#                 print "b file:"+str(lt[1]) +";a file:"+ str(uidcit[1])
            else:
                fp_ct+=1
    return  len(tp_uid_list), fp_ct

def roundHandler(fpath, batchstr, batchtype):
    sets_a = "a"
    sets_b = "b"
    uidlist_a, uidcity_list_a = loaddata(fpath, batchstr, batchtype, sets_a)
    uidlist_b, uidcity_list_b = loaddata(fpath, batchstr, batchtype, sets_b)
    labellist = getlabeluid(uidlist_a, uidlist_b)
    label_ct = len(labellist)
    print str(label_ct)
    tp_ct, fp_ct = getresult(uidcity_list_a, uidcity_list_b)
    print "precision: " + str(float(tp_ct) / float(tp_ct + fp_ct))
    print "recall: " + str(float(tp_ct) / float(label_ct))
    
if __name__ == '__main__':
    fpath = "./data/"
    batchtype = "new"
    for batchno in range(0,5):
        batchstr=str(batchno)
        roundHandler(fpath, batchstr, batchtype)