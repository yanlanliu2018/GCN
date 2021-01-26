#！/usr/bin/env python
#-*-coding:utf-8-*-

#以EntityID：EntityAttrEmedding(字典)的格式存入文件
#对实体名属性文本向量进行序列化，序列化格式：{id:attr_str_vec}
import pickle

from LYL.include.Config import Config

# dic = {"1":1,"2":2}
# if dic.keys().__contains__(1):
#     print("1")

path = './data/' + Config.language + '/attr_vect_cpm_2.txt'  # Ase（Attr_string_embedding)的向量文件，
with open(path, "rb+") as f:
    d = pickle.load(f)


for i in range(11000):
    if d.keys().__contains__(str(i)):
        print(i)
        print(d[str(i)])