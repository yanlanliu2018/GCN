#！/usr/bin/env python
#-*-coding:utf-8-*-
import pickle

import requests

# 方法一：只找到根据实体ID（Q51880772）进行查询的方法，没有找到根据关系ID（P373）查询信息的方法
# API_ENDPOINT = "https://www.wikidata.org/w/api.php"
#
# query = "Q51880772"
#
# params = {
#     'action': 'wbsearchentities',
#     'format': 'json',
#     'language': 'en',
#     'search': query
# }
#
# r = requests.get(API_ENDPOINT, params = params)
#
# print(r.json()['search'][0])

# 方法二：
from qwikidata.sparql  import return_sparql_query_results
import json

# 通过查询借口查询 实体/关系/属性 ID 对应的名称
def get_label(id):
    query_string = """SELECT * WHERE {
      wd:""" + id +""" rdfs:label ?label 
      FILTER (langMatches( lang(?label), "EN" ) )
    }"""

    print(id)
    result = ""
    try:
        res = return_sparql_query_results(query_string)
    except Exception as e:
        print(e)
        result = " "
        # 用来区别错误导致的值缺失还是本身缺失，
        # “” ： 本身缺失； “ ”：错误导致的缺失
    else:
        print(res["results"]["bindings"])
        if (res["results"]["bindings"].__len__() != 0):
            result = res["results"]["bindings"][0]['label']['value']

    return result

# 获取实验中 wikidata 数据需要的实体名
# 以 {"Q216789":"Commons category",......}的形式存储，使用json进行序列化
def getAllEntAndProName(inPaths,outPath):
    id_name = dict()

    for path in inPaths:
        with open(path,'r',encoding='utf-8') as file:
            nullNum = 0
            num = 0
            for line in file:
                num += 1
                print(line)
                id = line.split('\t')[1].split('/')[-1].split('\n')[0]
                name = get_label(id)
                id_name[id]=name

                if(name=="" or name==" "):
                    nullNum += 1
                    print("一共有" + str(nullNum) + "个数据是空值。")

                print(name)
                print("已经处理了"+str(num) + "条数据！")

            print("一共有" + str(nullNum) + "个数据是空值。")


    with open(outPath, 'w', encoding='UTF-8') as f:
        json.dump(id_name, f, ensure_ascii=False)

    print("数据处理结束！")

# 获取实验中 wikidata 数据需要的属性名
# 以 {"P373":"Commons category",......}的形式存储，使用json进行序列化
def getAllAttrName(inPath,outPath,attrIdsPath):
    id_attrName = dict()
    attrIds = set()

    # 遍历attr_tripples_2文件，获取所有不重复的属性id
    with open(inPath, 'r', encoding='utf-8') as file:
        num = 0
        for line in file:
            num += 1
            id = line.split('\t')[1].split('/')[-1].split('\n')[0]
            print(id)
            attrIds.add(id)
        print('一共有'+str(num)+'个属性三元组！')
        print('一共有'+str(attrIds.__len__())+'个属性！')

    with open(attrIdsPath, 'wb') as f:
        pickle.dump(attrIds, f)

    num = 0
    nullNum = 0
    for id in attrIds:
        num +=1
        attrName = get_label(id)
        id_attrName[id] = attrName
        if (attrName == "" or attrName == " "):
            nullNum += 1
            print("一共有" + str(nullNum) + "个数据是空值。")

        print(id +" "+ attrName)
        print("已经处理了" + str(num) + "条数据！")
    print("一共有" + str(nullNum) + "个数据是空值。")

    with open(outPath, 'w', encoding='UTF-8') as f:
        json.dump(id_attrName, f, ensure_ascii=False)

    print("数据处理结束！")

# 对于在getAllEntAndProName 中获取失败的信息进行重试补充
def supplementary_information(inPath):
    file = open(inPath,'r',encoding='utf-8')
    id_name = json.load(file)
    file.close()

    nullCount = 0 # 用来记录一共有多少个是空值“”
    lastNullCount = 0 # 用来记录有多少个依然为空值(由于错误导致的）

    for key,value in id_name.items():
        if(value == " "):
            nullCount += 1
            print("已经处理了"+ str(nullCount) + "条数据！")
            nameString = get_label(key)
            if(nameString == " "):
                lastNullCount += 1
            id_name[key] = nameString

    with open(inPath, 'w', encoding='UTF-8') as f:
        json.dump(id_name, f, ensure_ascii=False)

    print("一共有" + str(nullCount) + "条数据被处理。")
    print("还剩" + str(lastNullCount) + "条数据需要处理。")
    print("数据处理结束！")

def get_null_num(inPath):
    file = open(inPath, 'r', encoding='utf-8')
    id_name = json.load(file)
    file.close()

    nullCount = 0  # 用来记录一共有多少个是空值“ ”
    lastNullCount = 0  # 用来记录有多少个依然为空值(由于错误导致的）

    for key,value in id_name.items():
        if(value == ""):
            nullCount += 1
            print("已经处理了"+ str(nullCount) + "条数据！")
            nameString = get_label(key)
            if(nameString == " "):
                lastNullCount += 1
            id_name[key] = nameString

    with open(inPath, 'w', encoding='UTF-8') as f:
        json.dump(id_name, f, ensure_ascii=False)

if __name__=="__main__":
    # print(get_label("P373"))

    # inpaths = ["../../data/dbp_wd_15k_V1/mapping/0_3/ent_ids_2"]
    # outpath = "../../data/dbp_wd_15k_V1/mapping/0_3/ent_string_2.json"
    # getAllEntAndProName(inpaths,outpath)
    #
    # supplementary_information("../../data/dbp_wd_15k_V1/mapping/0_3/ent_string_2.json")

    inpath = "../../data/dbp_wd_15k_V1/attr_triples_2"
    outPath = "../../data/dbp_wd_15k_V1/attr_string_2.json"
    attrIdsPath = "../../data/dbp_wd_15k_V1/attrIds.pickle"

    # getAllAttrName(inPath=inpath,outPath=outPath,attrIdsPath=attrIdsPath)

    # supplementary_information(outPath)
    get_null_num(outPath)