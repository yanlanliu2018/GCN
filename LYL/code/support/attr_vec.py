import json
import pickle
import numpy as np

from LYL.code.support.bert_support import BertSupport


def getAttrVec1():
    '''
    获取文件1中所有实体的属性向量表示，
    以EntityID：EntityAttrEmedding(字典)的格式存入文件

    '''

    id_attrString = dict() #用于存储实体的属性信息，格式：{id:[“属性名 属性值”，。。。。。。]}
    name_attrString = dict() #用于存储实体的属性信息，格式：{实体名:[“属性名 属性值”，。。。。。。]}
    id_name = dict() #格式：{id:实体名，。。。。。。]}

    # 获取id_name字典
    with open("../../data/dbp_wd_15k_V1/mapping/0_3/ent_ids_1",'r',encoding='utf-8') as file:
        for line in file:
            # 0	http://dbpedia.org/resource/Jannie_du_Plessis
            lines = line.split('\t')
            id_name[lines[0]] = lines[1].split('\n')[0]

    path1 = "../../data/dbp_wd_15k_V1/attr_triples_1"
    print("现在开始获取" + path1 + "中实体属性的向量表示。")
    #获取 name_attrString 字典
    with open(path1,'r',encoding='utf-8') as file:
        for line in file:
            # http://dbpedia.org/resource/Philip_III_of_Spain	http://dbpedia.org/ontology/birthDate	"1578-04-14"^^<http://www.w3.org/2001/XMLSchema#date>
            lines = line.split('\t')
            name = lines[0]
            if(name_attrString.__contains__(name)):
                attrList = name_attrString[name]
                attrList.append(lines[1].split('/')[-1]+" "+lines[2].split('"')[1])
                name_attrString[name] = attrList
            else:
                attrList = []
                attrList.append(lines[1].split('/')[-1] + " " + lines[2].split('"')[1])
                name_attrString[name] = attrList

    # 获取每个实体的属性的向量表示
    id_list = [] # 存储所有id
    attr_string_list = [] #存储属性信息，每1000条实体，置空一次
    vect_list = [] # 存储所有属性信息的向量
    num = 0
    for id in id_name.keys():
        id_attrString[id] = name_attrString[id_name[id]]
        id_list.append(id)
        attr_string_list = attr_string_list + id_attrString[id]
        num+=1
        if(num%100 == 0):
            print("已经获取了" + str(num) + "条数据的属性向量。")
            vect_list = vect_list + (BertSupport().word_list_vector(wordList=attr_string_list))
            attr_string_list = []

    # 求取实体的平均属性向量,格式：{id:[平均向量，。。。。。。]}
    id_vec = dict()
    index = 0
    for id in id_list:
        count = id_attrString[id].__len__()
        nextIndex = index+count
        vect = np.zeros(shape=(1, 768), dtype=np.float32)
        if(count!=0):
            while index<nextIndex:
                vect += vect_list[index]
                index+=1
            vect = vect/count
        id_vec[id] = vect


    print("文件-" + path1 + "-获取实体属性向量结束！")

    outpath = "../../data/dbp_wd_15k_V1/attr_vect_cpm_1.txt"
    with open(outpath, "wb") as f:
        pickle.dump(id_vec, f)
    print("序列化结束！")


def getAttrVec2():
    '''
    获取文件2中所有实体的属性向量表示，
    以EntityID：EntityAttrEmedding(字典)的格式存入文件

    '''

    id_attrString = dict() #用于存储实体的属性信息，格式：{id:[“属性名 属性值”，。。。。。。]}
    name_attrString = dict() #用于存储实体的属性信息，格式：{实体名:[“属性名 属性值”，。。。。。。]}
    id_name = dict() #格式：{id:实体名，。。。。。。]}

    # 获取 attr_string 字典
    # attr_string = dict()
    path = "../../data/dbp_wd_15k_V1/attr_string_2.json"
    with open(path, "rb+") as f:
        attr_string = json.load(f)


    # 获取id_name字典
    with open("../../data/dbp_wd_15k_V1/mapping/0_3/ent_ids_2",'r',encoding='utf-8') as file:
        for line in file:
            # 10500	http://www.wikidata.org/entity/Q325033
            lines = line.split('\t')
            id_name[lines[0]] = lines[1].split('\n')[0]

    path2 = "../../data/dbp_wd_15k_V1/attr_triples_2"
    print("现在开始获取" + path2 + "中实体属性的向量表示。")
    #获取 name_attrString 字典
    with open(path2,'r',encoding='utf-8') as file:
        for line in file:
            # http://www.wikidata.org/entity/Q216789	http://www.wikidata.org/entity/P1263	"565/000095280"
            lines = line.split('\t')
            name = lines[0]
            if (name_attrString.__contains__(name)):
                attrList = name_attrString[name]
            else:
                attrList = []
            attr_name = attr_string[lines[1].split('/')[-1]]
            if (lines[2].split('"').__len__() > 1):
                attr_value = lines[2].split('"')[1]
            else:
                attr_value = lines[2]
            attrList.append(attr_name + " " + attr_value)
            name_attrString[name] = attrList

    # 获取每个实体的属性的向量表示
    id_list = [] # 存储所有id
    attr_string_list = [] #存储属性信息，每100条实体，置空一次
    vect_list = [] # 存储所有属性信息的向量
    num = 0
    for id in id_name.keys():
        id_attrString[id] = name_attrString[id_name[id]]
        id_list.append(id)
        attr_string_list = attr_string_list + id_attrString[id]
        num+=1
        if(num%100 == 0):
            print("已经获取了" + str(num) + "条数据的属性向量。")
            vect_list = vect_list + (BertSupport().word_list_vector(wordList=attr_string_list))
            attr_string_list = []

    # 求取实体的平均属性向量,格式：{id:[平均向量，。。。。。。]}
    id_vec = dict()
    index = 0
    for id in id_list:
        count = id_attrString[id].__len__()
        nextIndex = index+count
        vect = np.zeros(shape=(1, 768), dtype=np.float32)
        if(count!=0):
            while index<nextIndex:
                vect += vect_list[index]
                index+=1
            vect = vect/count
        id_vec[id] = vect


    print("文件-" + path2 + "-获取实体属性向量结束！")

    outpath = "../../data/dbp_wd_15k_V1/attr_vect_cpm_2.txt"
    with open(outpath, "wb") as f:
        pickle.dump(id_vec, f)
    print("序列化结束！")

def merge():
    # 将两个文件的 实体id-属性平均向量 字典合并在一起，并进行序列化
    path1 = "../../data/dbp_wd_15k_V1/attr_vect_cpm_1.txt"
    path2 = "../../data/dbp_wd_15k_V1/attr_vect_cpm_2.txt"
    with open(path1, "rb+") as f:
        vect1 = pickle.load(f)
    with open(path2, "rb+") as f:
        vect2 = pickle.load(f)

    print(vect1.__len__())
    print(vect2.__len__())

    vect1.update(vect2)
    print(vect1.__len__())
    path = "../../data/dbp_wd_15k_V1/attr_vect_cpm.txt"
    with open(path, "wb") as f:
        vect1 = pickle.dump(vect1, f)



if __name__ == "__main__":

    getAttrVec1()
    getAttrVec2()
    merge()