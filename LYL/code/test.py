#！/usr/bin/env python
#-*-coding:utf-8-*-
# nameId = int('3')
# print(nameId)
#
# s = "0	http://dbpedia.org/resource/Jannie_du_Plessis"
# lines = s.split('\t')
# nameString = lines[1].split('/')[-1]
# nameId = int(lines[0])
# print(nameId)
# print(nameString)
#
# for i in range(len(lines)):
#     print(i)

# id_name = dict()
# id = "345"
# name = "hahah"
# id_name[id] = name
#
#
# l = [1,2,3]
# print(l.__len__())

# di = {"1":1,"2":2}
# for key,value in di.items():
#     if(value == 2):
#         di[key] = value*2
#
# for key,value in di.items():
#     print(key)
#     print(value)
#     print("...............................")

# import requests
#
# API_ENDPOINT = "https://www.wikidata.org/w/api.php"
#
# query = "Q84287"
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

for i in range(5):
    print(i)