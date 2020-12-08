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

    res = return_sparql_query_results(query_string)

    result = res["results"]["bindings"][0]['label']['value']
    # print(result)
    return result

    # for row in res["results"]["bindings"]:
    #     print(row)
    #     print(row.__class__)
    #     print(row['label']['value'])
        # print(row["value"])

# 获取实验中 wikidata 数据需要的实体名和属性名
# 以 {"P373":"Commons category",......}的形式存储，使用json进行序列化
def getAllEntAndProName(inPaths,outPath):
    id_name = dict()

    for path in inPaths:
        with open(path,'r','utf-8') as file:
            for line in file:
                id = line.split('\t')[1].split('/')[-1]
                name = get_label(id)
                dict[id]=name


    with open(outPath, 'w', encoding='UTF-8') as f:
        json.dump(id_name, f, ensure_ascii=False)


if __name__=="__main__":
    # print(get_label("P373"))
    inpaths = ["",""]
    outpath = ""
    getAllEntAndProName(inpaths,outpath)