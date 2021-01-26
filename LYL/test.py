from LYL.include.Config import Config
import tensorflow as tf
from LYL.include.Model import build_SE, training, combine
from LYL.include.Test import get_hits, get_hits_select, get_combine_hits_select_correct, solely_measure
from LYL.include.Load import *
import copy
import numpy as np
import math
import pickle

def id2degree():
	path = './data/' + Config.language + '/mapping/0_3/triples_1'
	inf2 = open(path)
	id2fre = dict()  # 用来记录实体节点的度（包括入度和出度）  {节点id：度，。。。}
	for line in inf2:
		strs = line.strip().split('\t')  # 23883	157	2572，实体id-关系id-实体id

		# 统计头节点的出度
		if strs[0] not in id2fre:
			fre = 0
		else:
			fre = id2fre[strs[0]]
		fre += 1
		id2fre[strs[0]] = fre

		# 统计尾节点的入度
		if strs[2] not in id2fre:
			fre1 = 0
		else:
			fre1 = id2fre[strs[2]]
		fre1 += 1
		id2fre[strs[2]] = fre1
	return id2fre


id2fre = id2degree()  ##只对知识库1的数据进行度的统计
e = len(set(loadfile(Config.e1, 1)) | set(loadfile(Config.e2, 1)))  # 获取并集，也就是两个图谱中的所有实体id，用一个list存储。
ILL = loadfile(Config.ill, 2)  # 将可对齐实体对加载到list中，[[e11,e21],[e12,e22]]
illL = len(ILL)
# np.random.shuffle(ILL) #重排序返回随机序列
train = ILL[:int(math.floor(illL * Config.seed))]  # 获取ILL中的前n条数据，n是一个随机数
# train = sortbydegree(train, id2fre)  # 根据度对训练数据进行排序，返回的数据依然是对齐实体对，实体id-实体id
train_array = np.array(train)  # 使用np.array将list数组化，便于科学计算
test = ILL[int(math.floor(illL * Config.seed)): int(math.floor(illL * (Config.seed + 0.07)))]  # 测试数据取训练数据后的0.07%
test = ILL[int(math.floor(illL * (Config.seed + 0.07))):]  # 测试数据取剩余数据

KG1 = loadfile(Config.kg1, 3);
KG2 = loadfile(Config.kg2, 3)  # 加载图谱的三元组数据，[[实体id，关系id，实体id]...]
storepath = './result/' + Config.language + '/'
# np.save(storepath + 'train.npy', train_array); np.save(storepath + 'test.npy', test)  # 将数组以二进制格式保存在“.npy”文件中。
outfile = open(storepath + 'record.txt', 'w')  # 创建输出文件“record.txt”


print('LOAD ASE...')
print('Result of ASE:')
outfile.write('Result of ASE:\n')
asepath = './data/' + Config.language + '/attr_vect_cpm.txt'  # Ase（Attr_string_embedding)的向量文件，
ase_vec = loadAse(asepath)  # 加载实体属性文本向量所在文件，获取向量矩阵
np.save(storepath + '/ase_vec.npy', ase_vec)  # 以文件的形式保存数组
solely_measure(ase_vec, test, 768)  # 单独测量，也就是测量只使用实体名向量来进行对齐的效果


# # build
# ite_counter = 0
# output_layer, loss = build_SE(Config.se_dim, Config.act_func, Config.gamma, Config.k, e, train_array, KG1 + KG2)
# se_vec, J = training(output_layer, loss, 25, Config.epochs_se, train_array, e, Config.k)
# print('loss:', J)
# # np.save(storepath+ 'se_vec_test_ini.npy', se_vec)
# # se_vec = np.load(storepath+ 'se_vec_test_ini.npy')
#
# print('Result of SE:')
# #outfile.write('Result of SE:\n')
# solely_measure(se_vec, test, 768)
# #outfile.flush()