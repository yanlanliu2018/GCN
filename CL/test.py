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

# l = []
# s = np.fromstring('1,2',sep=',')
# print(s)
# l.append(s)
# s = np.fromstring('1,2',sep=',')
# print(s)
# l.append(s)
#
# n = np.hstack(l)
# print(n)

# import tensorflow as tf
#
# def cal_performance(ranks, top=10):
#     m_r = sum(ranks) * 1.0 / len(ranks)
#     h_10 = sum(ranks <= top) * 1.0 / len(ranks)
#     mrr = (1. / ranks).sum() / len(ranks)
#     return m_r, h_10, mrr
#
# dim = 3
#
# vec = {1:[1,2,3],2:[4,5,6],3:[7,8,9],3:[10,11,12],4:[13,14,15],5:[16,17,18],6:[19,20,21]}
# test_pair = [[1,2],[1,4],[5,6]]
#
#
# Lvec = tf.placeholder(tf.float32, [None, dim]) # 获取对齐实体对头节点的
# Rvec = tf.placeholder(tf.float32, [None, dim])
#
# # he = tf.nn.l2_normalize(Lvec, dim=-1) #??? 规范化啊
# # norm_e_em = tf.nn.l2_normalize(Rvec, dim=-1)
# aep = tf.matmul(Lvec, Rvec) # 两个矩阵相乘，得到的矩阵是：头节点个数*尾节点个数
#
# sess = tf.Session()
# Lv = np.array([vec[e1] for e1, e2 in test_pair]) # 获取对齐实体对头节点的向量表示的列表
# Lid_record = np.array([e1 for e1, e2 in test_pair]) # 获取对齐实体对头节点的实体id值
# Rv = np.array([vec[e2] for e1, e2 in test_pair]) # 获取对齐实体对尾节点的向量表示的列表
# Rid_record = np.array([e2 for e1, e2 in test_pair]) # 获取对齐实体对尾节点的实体id值
# aep_fuse = sess.run(aep, feed_dict = {Lvec: Lv, Rvec: Rv})
# c = Rv[range(3),range(3)]
# d = c.reshape(3,1)
# e = Rv - d
#
# a = aep_fuse[range(len(Lid_record)), range(len(Lid_record))]
# b = a.reshape(len(aep_fuse), 1)
#
# probs = aep_fuse - aep_fuse[range(len(Lid_record)), range(len(Lid_record))].reshape(len(aep_fuse), 1)
# # only rank those who have correspondings... cause the set is distorted for those above max_correct
# ranks = (probs >= 0).sum(axis=1)
# print('to be evaluated... ' + str(len(ranks)))
#
# MR, H10, MRR = cal_performance(ranks, top=10)
# _, H1, _ = cal_performance(ranks, top=1)
#
# msg = 'Soly measure: Hits@1:%.3f, Hits@10:%.3f, MR:%.3f, MRR:%.3f' % (H1, H10, MR, MRR)
# print('\n'+msg)

# top = 2
# probs = np.array([[-1,2,3],[-4,5,6],[7,8,9]])
# print(probs)
# ranks = (probs >= 0).sum(axis=1)
# print(ranks)
# m_r = sum(ranks) * 1.0 / len(ranks)  # m_r：
# print(sum(ranks))
# print(m_r)
# h_10 = sum(ranks <= top) * 1.0 / len(ranks)  # h_10: 前10个实体中包含正确实体的比例
# print(sum(ranks <= top))
# print(h_10)
# mrr = (1. / ranks).sum() / len(ranks)  # mrr：平均排序倒数
# print((1. / ranks).sum())
# print(mrr)


from scipy.spatial.distance import cdist

vec = {1:[1,2,3],2:[4,5,6],3:[7,8,9],3:[10,11,12],4:[13,14,15],5:[16,17,18],6:[19,20,21]}
test_pair = [[1,2],[1,4],[5,6]]

test = np.array(test_pair)

print(test)
print(test.shape[0])

Lvec = np.array([vec[e1] for e1, e2 in test_pair])
Lid_record = np.array([e1 for e1, e2 in test_pair])
Rvec = np.array([vec[e2] for e1, e2 in test_pair])
Rid_record = np.array([e2 for e1, e2 in test_pair])

sim = cdist(Lvec, Rvec, metric='cityblock')
print(Lvec)
print(Rvec)
print(sim)

print(sim[2, :])
print(sim[2, :].argsort())

for i in range(Lvec.shape[0]):
    rank = sim[i, :].argsort()
    rank_index = np.where(rank == i)[0][0]
    r = np.where(rank==i)
    rr = np.where(rank==i)[0]
    print(rank == i)
    print(np.where(rank == i)[0])
    print(rank)
    print(rank_index)

top_k=(1, 10, 50, 100)
top_lr = [0] * len(top_k)
print(top_lr)

print(test.shape[0])

# a = [0,2,3,2,1,2,4,5,6,7,8,6,5,4,3,2,7,8,9,6,5,7,8,9,6,9,1,2,2,5,6,8,8,9,7,0]
# x = np.array(a)
# print(x)
# print(x[1])
# print(np.where(x>=5))  #输出x中大于等于5的元素的下标
# print(np.where(x>=5)[0]) #输出
# print(np.where(x>=5)[0][0])
# print('type np.where(x>=5):', type(np.where(x>=5)))
# print('type np.where(x>=5)[0]:', type(np.where(x>=5)[0]))
# digit_indices = [np.where(x == i)[0] for i in range(10)] #输出的是一个list，list里每个元素都是元组，元组里的第一个元素是list，具体看下面输出
# print('digit_indices:', type(digit_indices))
# print('digit_indices:', digit_indices)