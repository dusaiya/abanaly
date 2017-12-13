# encoding: utf-8
'''
Created on 2017年11月29日

@author: alibaba

'''
import numpy as np
import json

def loaddata(fpath,batchstr,batchtype,sets):
    uidlist = np.loadtxt(fpath + 'uidlist_' + batchtype + "_" + batchstr + "_" + sets, dtype=np.str, delimiter="\t")
    weibolist = np.loadtxt(fpath + 'weibolist_' + batchtype + "_" + batchstr + "_" + sets, dtype=np.str, delimiter="\t")
    return uidlist,weibolist[:,0:2]

def get_weibolist_by_uid(uid,weibolist):
    '''
    根据uid抽取微博
    '''
    ts=np.where(weibolist==uid)
    lts=weibolist[ts[0],1]
    return lts

def ele_ct_sort(lts):
    '''
    Parameters
    ----------
    #无序微博列表 lts 是 numpy.ndarray
    
    Returns
    -------
    eles 排序后的元素列表
    ele_ct 每个元素的个数
    total_ct 总的微博数
    bin_ct 元素的个数
    '''
    eles,cts=np.unique(lts,  return_counts=True)
    idx=np.argsort(-cts)
    return eles[idx],cts[idx],len(lts),len(idx)

def save2file(fpath, batchstr, batchtype, sets, uidlist, weibolist):
    '''
    将全部地址作为分类
    '''
    fout = open(fpath + "uid_city_" + batchtype + "_" + batchstr + "_" + sets, "wb")
    for uid in uidlist: #获取无序微博列表 lts 是 numpy.ndarray
        lts = get_weibolist_by_uid(uid, weibolist) #统计,并按从大到小顺序排序
        eles, ele_ct, total_ct, bin_ct = ele_ct_sort(lts)
        fout.write(str(uid) + "\t")
#         fout.write(str(total_ct) + "\t")
#         fout.write(str(bin_ct) + "\t")
        for ele_id in range(len(eles)):
            fout.write(str(eles[ele_id]))
        fout.write("\n")
    fout.close()

def save2file_bin(fpath, batchstr, batchtype, sets, uidlist, weibolist):
    '''
    输出 \t分割的数据，不推荐使用
    '''
    fout = open(fpath + "uid_city_bin_" + batchtype + "_" + batchstr + "_" + sets, "wb")
    fout_common=open(fpath + "uid_city_common_" + batchtype + "_" + batchstr + "_" + sets, "wb")
    
    for uid in uidlist: #获取无序微博列表 lts 是 numpy.ndarray
        lts = get_weibolist_by_uid(uid, weibolist) #统计,并按从大到小顺序排序
        eles, ele_ct, total_ct, bin_ct = ele_ct_sort(lts)
        if bin_ct==0:
            print "zero bin_ct, uid:" + str(uid)
            continue
        eles_mean=float(1)/float(bin_ct+1)#这里+1，防止城市过于少的情况，两个城市相差不多也会被忽略一个城市
        fout.write(str(uid) + "\t")
        fout.write(str(total_ct) + "\t")
        fout.write(str(bin_ct) + "\t")
        common_set=[]
        for ele_id in range(len(eles)):
            fout.write(str(eles[ele_id])+"\t")
            fout.write(str(ele_ct[ele_id])+"\t")
            if float(ele_ct[ele_id])/float(total_ct)>=eles_mean:
                common_set.append(str(eles[ele_id]))
        fout.write("\n")
        fout_common.write(str(uid) + "\t")
        for ele in sorted(common_set):
            fout_common.write(str(ele))
        fout_common.write("\n")  
    fout.close()
    fout_common.close()

def save2file_dict(fpath, batchstr, batchtype, sets, uidlist, weibolist):
    fout = open(fpath + "uid_city_bin_" + batchtype + "_" + batchstr + "_" + sets, "wb")
    fout_common=open(fpath + "uid_city_common_" + batchtype + "_" + batchstr + "_" + sets, "wb")
    
    for uid in uidlist: #获取无序微博列表 lts 是 numpy.ndarray
        lts = get_weibolist_by_uid(uid, weibolist) #统计,并按从大到小顺序排序
        eles, ele_ct, total_ct, bin_ct = ele_ct_sort(lts)
        if bin_ct==0:
            print "zero bin_ct, uid:" + str(uid)
            continue
        eles_mean=float(1)/float(bin_ct+1)#这里+1，防止城市过于少的情况，两个城市相差不多也会被忽略一个城市
        uid_dict={}
        uid_dict["uid"]=str(uid)
        uid_dict["total_ct"]=total_ct
        uid_dict["bin_ct"]=bin_ct
        citys=[]
        common_set=[]
        for ele_id in range(len(eles)):
            city_ob={}
            city_ob["city"]=str(eles[ele_id])
            city_ob["city_ct"]=ele_ct[ele_id]
            citys.append(city_ob)
            if float(ele_ct[ele_id])/float(total_ct)>=eles_mean:
                common_set.append(str(eles[ele_id]))
        uid_dict["citys"]=citys
        fout.write(json.dumps(uid_dict))
        fout.write("\n")
        fout_common.write(str(uid) + "\t")
        for ele in sorted(common_set):
            fout_common.write(str(ele))
        fout_common.write("\n")  
    fout.close()
    fout_common.close()
 
    
def roundHandler(fpath, batchstr, batchtype):
    sets_a = "a"
    sets_b = "b"
    #加载数据
    uidlist_a, weibolist_a = loaddata(fpath, batchstr, batchtype, sets_a)
    uidlist_b, weibolist_b = loaddata(fpath, batchstr, batchtype, sets_b)
    #纯用地址作为tag进行分类
    save2file(fpath, batchstr, batchtype, sets_a, uidlist_a, weibolist_a)
    save2file(fpath, batchstr, batchtype, sets_b, uidlist_b, weibolist_b)
#     save2file_bin(fpath, batchstr, batchtype, sets_a, uidlist_a, weibolist_a)
#     save2file_bin(fpath, batchstr, batchtype, sets_b, uidlist_b, weibolist_b)
    #输出城市字典
    save2file_dict(fpath, batchstr, batchtype, sets_a, uidlist_a, weibolist_a)
    save2file_dict(fpath, batchstr, batchtype, sets_b, uidlist_b, weibolist_b)

if __name__ == '__main__':
    fpath = "./data2/"
    batchtype = "new"
    for batchno in range(0,5):
        batchstr=str(batchno)
        roundHandler(fpath, batchstr, batchtype)
        
        