#！/usr/bin/env python
#-*-coding:utf-8-*-

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
    else:
        print(res["results"]["bindings"])
        if (res["results"]["bindings"].__len__() != 0):
            result = res["results"]["bindings"][0]['label']['value']

    return result

# 获取实验中 wikidata 数据需要的实体名和属性名
# 以 {"P373":"Commons category",......}的形式存储，使用json进行序列化
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

                if(name==""):
                    nullNum += 1
                    print("一共有" + str(nullNum) + "个数据是空值。")

                print(name)
                print("已经处理了"+str(num) + "条数据！")

            print("一共有" + str(nullNum) + "个数据是空值。")


    with open(outPath, 'w', encoding='UTF-8') as f:
        json.dump(id_name, f, ensure_ascii=False)

    print("数据处理结束！")


if __name__=="__main__":
    # print(get_label("P373"))
    inpaths = ["../../data/dbp_wd_15k_V1/mapping/0_3/ent_ids_2"] # "../../data/dbp_wd_15k_V1/mapping/0_3/ent_ids_2",
    outpath = "../../data/dbp_wd_15k_V1/mapping/0_3/ent_string_2.json"
    getAllEntAndProName(inpaths,outpath)
    # path = "../../data/dbp_wd_15k_V1/mapping/0_3/rel_ids_2"
    # file = open(path,'r',encoding='utf-8')
    # num = 0
    # while num<10:
    #     print(file.readline())
    #     num+=1