# encoding: utf-8
'''
Created on 2017年11月30日

@author: alibaba



'''
import numpy as np

def loaddata(fpath, batchstr, batchtype, sets):
    uidcity_list = np.loadtxt(fpath + 'uid_city_common_' + batchtype + "_" + batchstr + "_" + sets, dtype=np.str, delimiter="\t")
    return  uidcity_list

def getresult(uidcity_list_a, uidcity_list_b,fpath, batchstr, batchtype):
    fout = open(fpath + "uid_city_candidate_" + batchtype + "_"  + batchstr, "wb")
    for uidcit in uidcity_list_a:
        ts=np.where(uidcity_list_b==uidcit[1])
        lts=uidcity_list_b[ts[0],:]
        for lt in lts:
            fout.write(str(uidcit[0])+"\t"+str(lt[0])+"\n")

def roundHandler(fpath, batchstr, batchtype):
    sets_a = "a"
    sets_b = "b"
    uidcity_list_a = loaddata(fpath, batchstr, batchtype, sets_a)
    uidcity_list_b = loaddata(fpath, batchstr, batchtype, sets_b)
    getresult(uidcity_list_a, uidcity_list_b,fpath, batchstr, batchtype)
    
if __name__ == '__main__':
    fpath = "./data2/"
    batchtype = "new"
    for batchno in range(0,5):
        batchstr=str(batchno)
        roundHandler(fpath, batchstr, batchtype)