# encoding: utf-8
'''
Created on 2017年11月30日

@author: alibaba



'''
import numpy as np
import json
from scipy import stats
import math

def loaduid(fpath, batchstr, batchtype):
    sets_a = "a"
    sets_b = "b"
    candidate =np.loadtxt(fpath + "uid_city_candidate_" + batchtype + "_"  + batchstr , dtype=np.str, delimiter="\t")
    
    fin_a = open(fpath + 'uid_city_bin_' + batchtype + "_" + batchstr + "_" + sets_a)
    uid_bin_dict_a={}
    for line in fin_a.readlines():
        tmp_dict=json.loads(line)
        uid_bin_dict_a[tmp_dict["uid"]]=tmp_dict
    uid_bin_dict_b={}
    fin_b = open(fpath + 'uid_city_bin_' + batchtype + "_" + batchstr + "_" + sets_b)
    for line in fin_b.readlines():
        tmp_dict=json.loads(line)
        uid_bin_dict_b[tmp_dict["uid"]]=tmp_dict
#     uidlist_a = np.loadtxt(fpath + 'uidlist_' + batchtype + "_" + batchstr + "_" + sets_a, dtype=np.str, delimiter="\t")
#     uidlist_b = np.loadtxt(fpath + 'uidlist_' + batchtype + "_" + batchstr + "_" + sets_b, dtype=np.str, delimiter="\t")
    fin_a.close()
    fin_b.close()
    return uid_bin_dict_a,uid_bin_dict_b,candidate

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


def kendalltau4city(uid_bin_dict_a, uid_bin_dict_b, candi):
    tmp_dict_a = uid_bin_dict_a[str(candi[0])]
    tmp_dict_b = uid_bin_dict_b[str(candi[1])]
    if tmp_dict_a["bin_ct"] <= tmp_dict_b["bin_ct"]:
        bin_ct = tmp_dict_a["bin_ct"]
    else:
        bin_ct = tmp_dict_b["bin_ct"]
    city_list_a = []
    city_list_b = []
    for i in range(bin_ct):
        city_list_a.append(tmp_dict_a["citys"][i]["city"])
        city_list_b.append(tmp_dict_b["citys"][i]["city"])
    
    tmp_result = stats.kendalltau(np.array(city_list_a), np.array(city_list_b), nan_policy="propagate")
    score = tmp_result.correlation
    return score


def gen_probability(uid_bin_dict_a, uid_bin_dict_b,candi):
    '''
            根据城市发帖词频，统计出现概率
    '''
    tmp_dict_a = uid_bin_dict_a[str(candi[0])]
    tmp_dict_b = uid_bin_dict_b[str(candi[1])]
    source_ct = tmp_dict_a["total_ct"] # 总数
    city_dict_a = {}
    city_list_all = []
    for city in tmp_dict_a["citys"]:
        city_name = city["city"]
        city_dict_a[city_name] = float(city["city_ct"]) / float(source_ct)
        if city_name not in city_list_all:
            city_list_all.append(city_name)
    
    city_dict_b = {}
    for city in tmp_dict_b["citys"]:
        city_name = city["city"]
        city_dict_b[city_name] = float(city["city_ct"]) / float(source_ct)
        if city_name not in city_list_all:
            city_list_all.append(city_name)
    
    return city_list_all, city_dict_a, city_dict_b


def get_pair_probability(city_dict_a, city_dict_b, city_name):
    '''
    获取莫城市的概率，处理无key得情况
    '''
    if city_dict_a.has_key(city_name):
        probability_a = city_dict_a[city_name]
    else:
        probability_a = float(0)
    if city_dict_b.has_key(city_name):
        probability_b = city_dict_b[city_name]
    else:
        probability_b = float(0)
    return probability_a, probability_b

def hellinger_distance(uid_bin_dict_a, uid_bin_dict_b, candi):
    ##https://en.wikipedia.org/wiki/Hellinger_distance
    city_list_all, city_dict_a, city_dict_b = gen_probability(uid_bin_dict_a, uid_bin_dict_b,candi)
    score=float(0)
#     print city_dict_a
#     print city_dict_b
    for city_name in city_list_all:
        probability_a, probability_b = get_pair_probability(city_dict_a, city_dict_b, city_name)
        score+=np.power(math.sqrt(probability_a)-math.sqrt(probability_b),2)
        
    return math.sqrt(score/float(2))

def candidate_filter(func,uid_bin_dict_a,uid_bin_dict_b,candidate,fpath, batchstr, batchtype):
    fout=open(fpath + "uid_city_result_"+str(func.func_name)+"_" + batchtype + "_"  + batchstr,"wb")
    for candi in candidate:
        score = func(uid_bin_dict_a, uid_bin_dict_b, candi)
        fout.write(str(candi[0])+"\t"+str(candi[1])+"\t"+str(score)+"\n")
    fout.close()
#     filter_result =np.loadtxt(fpath + "uid_city_result_" + batchtype + "_"  + batchstr +"_"+str(kd_threshold),
#                               dtype=np.str, delimiter="\t")
#     print filter_result.shape
#     return filter_result
    
def roundHandler(func,fpath, batchstr, batchtype):
    ## uid_bin_dict为查找字典
    uid_bin_dict_a,uid_bin_dict_b,candidate = loaduid(fpath, batchstr, batchtype)
    candidate_filter(func,uid_bin_dict_a,uid_bin_dict_b,candidate,fpath, batchstr, batchtype)
#     filter_len,tmp_row=filter_result.shape
#     correct_ct=0
#     for tmp_result in filter_result:
#         if tmp_result[0]==tmp_result[1]:
#             correct_ct+=1
#     label_list=getlabeluid(uidlist_a, uidlist_b)
#     label_ct=len(label_list) ##符合的数据
#     ## 筛选符合条件的结果集
#     print "precision: " + str(float(correct_ct) / float(filter_len))
#     print "recall: " + str(float(correct_ct) / float(label_ct))
    
if __name__ == '__main__':
    fpath = "./data2/"
    batchtype = "new"
    for batchno in range(0,5):
        batchstr=str(batchno)
        #kendalltau4city
#         roundHandler(kendalltau4city,fpath, batchstr, batchtype)
        #hellinger_distance
        roundHandler(hellinger_distance,fpath, batchstr, batchtype)
        