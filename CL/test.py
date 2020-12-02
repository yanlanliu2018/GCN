# map = {'n':1,'j':2}
# for r in map:
#     print(r)

# e = 10
# du = [1] * e
# print(du)
import math
# path = './data/' + 'dbp_wd_15k_V1' + '/mapping/0_3/triples_1'
# inf2 = open(path)
# id2fre = dict()
# for i in range(10):
#     line = inf2.readline()
#     strs = line.strip().split('\t')
#     print(line)
#     print(strs)
#

# s1 = {1,2,3}
# s2 = {4,5,6}
# print(s1 | s2)
# num=1
# for i in range(num):
#     print(i)
#
# path = './data/' + 'dbp_wd_15k_V1' + '/mapping/0_3/triples_1'
# f1 = open(path)
# vectors = []
# # enumerate(): 将可遍历对象组合为一个索引序列，同时列出数据和数据下标
# line_nu = 0
# for i, line in enumerate(f1):
#     if line_nu < 5:
#         print(i)
#         print(line)
#         line_nu += 1
#     else:
#         break

import numpy as np

l = []
s = np.fromstring('1,2',sep=',')
print(s)
l.append(s)
s = np.fromstring('1,2',sep=',')
print(s)
l.append(s)

n = np.hstack(l)
print(n)
