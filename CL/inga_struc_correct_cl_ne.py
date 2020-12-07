from CL.include.Config import Config
import tensorflow as tf
from CL.include.Model import build_SE, training, combine
from CL.include.Test import get_hits, get_hits_select, get_combine_hits_select_correct, solely_measure
from CL.include.Load import *
import copy
import numpy as np
import math
import pickle

# load sorted training data by degree(difficulty)
# 按程度(难度)排序的训练数据
def id2degree():
	path = './data/' + Config.language + '/mapping/0_3/triples_1'
	inf2 = open(path)
	id2fre = dict()  # 用来记录实体节点的度（包括入度和出度）
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

# train：难道是每一轮迭代训练中被选中的训练集合（已知对齐实体）
#id2fre：记录实体节点的度
def sortbydegree(train, id2fre):
	left2degree = dict() # 用来记录已对齐实体头节点对应的度
	left2right = dict() # 用来记录已对齐实体对，实体id-实体id
	for item in train:
		left2right[item[0]] = item[1]
		left2degree[item[0]] = id2fre[str(item[0])]

	list1= sorted(left2degree.items(),key=lambda x:x[1], reverse=True) #降序
	# https://www.runoob.com/python/python-func-sorted.html

	newtrain = []
	for item in list1:
		newtrain.append(tuple([item[0], left2right[item[0]]]))
	# 返回已经根据度做好排序的训练集合
	return newtrain

#
def non_rep_match(test, train, index1, index2, gap1, gap2, ranks1, dicrank,id2fre, kkk):
	coun = 0	#
	truecounter = 0		#
	newtest = copy.deepcopy(test)	#新的测试集合
	newtestleft = [	]	#测试集合头节点
	newtestright = [ ]	#测试集合尾节点
	for item in newtest:
		newtestleft.append(item[0])
		newtestright.append(item[1])

	# i：第i个头节点
	# index1[i]：第i个头节点向量距离最近的尾节点下标j
	# index2[index1[i]]：与第j个尾节点向量距离最近的头节点下标
	# 找到高置信度且课程难度在设置范围内的实体对，加入训练集，并从测试集中剔除
	for i in range(len(index1)):
		if index1[i] < len(index2):
			if index2[index1[i]] == i:
				# 0.03：实验参数设置的θ１
				if gap1[i] >= 0.03 and gap2[i] >= 0.03:
					if id2fre[str(test[i][0])] >= kkk: # kkk：基于课程的迭代策略中，表示课程难度的实体节点度数值
						coun += 1
						# dicrank[头节点id] = 头节点正确匹配的尾节点的排序
						dicrank[str(test[i][0])] = ranks1[i]
						train.append(tuple([int(test[i][0]), int(test[index1[i]][1])])) # 将与第i个头节点相似度最高的实体对加入训练集，可能会存在错误匹配的实体对
						newtestleft.remove(int(test[i][0])) # 从头节点的集合中剔除对应头节点
						newtestright.remove(int(test[index1[i]][1])) # 从头节点的集合中剔除对应尾节点
						#newtest.remove(tuple([int(test[i][0]), int(test[i][1])]))
						if test[i][0] + 10500 == test[index1[i]][1]:
							truecounter += 1
	print(coun)
	print(truecounter)

	test = []
	excludedleft = []; excludedright = []
	for item in newtestleft:
		if item + 10500 in newtestright:
			test.append(tuple([item, item + 10500])) # 加入剩余的头节点中能够正确对齐的实体对
		else:
			excludedleft.append(item) # item 的匹配尾节点被错误剔除，将 item 加入到 excludedleft 中
	max_correct = len(test) # 可正确对齐的实体对最大数量

	for item in newtestright:
		if item - 10500 not in newtestleft:
			excludedright.append(item)
	assert len(excludedleft) == len(excludedright) # 判断，若等式不成立汇报错
	for i in range(len(excludedleft)):
		test.append(tuple([excludedleft[i], excludedright[i]])) # 将头节点和尾节点中无法正确匹配的实体对按序组成实体对，加入test的末尾，作为待对齐但是无法找到正确匹配的头节点/尾节点
	### really fucking complicated

	return train, test, max_correct, dicrank


seed = 12306
np.random.seed(seed)  # 每次使用相同的随机数种子seed，则生成的随机数相同。np.random.random()或者np.random.rand(4,3)
tf.set_random_seed(seed) # 与前面的效果相同

if __name__ == '__main__':
	id2fre = id2degree()
	e = len(set(loadfile(Config.e1, 1)) | set(loadfile(Config.e2, 1))) # 获取并集，也就是两个图谱中的所有实体id，用一个list存储。
	ILL = loadfile(Config.ill, 2) # 将可对齐实体对加载到list中，[[e11,e21],[e12,e22]]
	illL = len(ILL)
	#np.random.shuffle(ILL) #重排序返回随机序列
	train = ILL[:int(math.floor(illL* Config.seed))] #获取ILL中的前n条数据，n是一个随机数
	#train = sortbydegree(train, id2fre)  # 根据度对训练数据进行排序，返回的数据依然是对齐实体对，实体id-实体id
	train_array = np.array(train) # 使用np.array将list数组化，便于科学计算
	test = ILL[int(math.floor(illL* Config.seed)): int(math.floor(illL* (Config.seed + 0.07)))] #测试数据取训练数据后的0.07%
	test = ILL[int(math.floor(illL* (Config.seed + 0.07))):] #测试数据取剩余数据

	KG1 = loadfile(Config.kg1, 3) ; KG2 = loadfile(Config.kg2, 3) #加载图谱的三元组数据，[[实体id，关系id，实体id]...]
	storepath = Config.language + '/'
	#np.save(storepath + 'train.npy', train_array); np.save(storepath + 'test.npy', test)  # 将数组以二进制格式保存在“.npy”文件中。
	outfile = open(storepath+ 'record.txt', 'w')  # 创建输出文件“record.txt”

	print('LOAD NE...')
	print('Result of NE:')
	#outfile.write('Result of NE:\n')
	nepath = './data/'+ Config.language + '/mapping/0_3/name_vec_cpm_3.txt'  #Ne（Name_embedding)的向量文件，
	ne_vec = loadNe(nepath)  # 加载实体名向量所在文件，获取向量矩阵
	#np.save(storepath + '/ne_vec.npy', ne_vec)  # 以文件的形式保存数组
	solely_measure(ne_vec, test, 900) # 单独测量，也就是测量只使用实体名向量来进行对齐的效果

	# build
	ite_counter = 0
	# output_layer, loss = build_SE(Config.se_dim, Config.act_func, Config.gamma, Config.k, e, train_array, KG1 + KG2)
	# se_vec, J = training(output_layer, loss, 25, Config.epochs_se, train_array, e, Config.k)
	# print('loss:', J)
	# np.save(storepath+ 'se_vec_test_ini.npy', se_vec)
	se_vec = np.load(storepath+ 'se_vec_test_ini.npy')

	print('Result of SE:')
	#outfile.write('Result of SE:\n')
	#solely_measure(se_vec, test, 900)
	#outfile.flush()

	dicrank = dict()
	# index1：被认为和头节点匹配的尾节点的下标（向量距离最近的节点）
	# gap1：probs中每一行最大值和第二大的值之间的差，即与头节点之间的距离最近的尾节点和第二近尾节点之间的相似度之差（距离之差）
	# truths1：能够找到正确实体对的头节点的下标值
	# ranks1：可正确对齐的尾节点在相似度中的排序值
	index1, gap1, truths1, ranks1, index2, gap2, truths2, ranks2 = get_combine_hits_select_correct(se_vec, ne_vec, test, dicrank, len(test))


	# 之前被作者注释掉的代码的起始点
	# addnewents
	trainlength_old = len(train)
	# 获取新的训练集、测试集、最大可对齐实体对数、dicrank[头节点id] = 头节点正确匹配的尾节点的排序
	train, test, max_correct, dicrank = non_rep_match(test, train, index1, index2, gap1, gap2, ranks1, dicrank, id2fre, 10)
	#train = sortbydegree(train)
	train_array = np.array(train)

	print('len of new train/seed: ' + str(len(train)))
	print('len of new test: ' + str(len(test)))
	print('len of max correct in the test: ' + str(max_correct))
	np.save(storepath + 'train.npy', train)
	np.save(storepath + 'test.npy', test)
	df2=open(storepath + 'dicrank.npy','wb')
	pickle.dump(dicrank,df2) # 序列化，将对象 dicrank 保存到文件 df2 中

	# kkk：课程难度的迭代值
	# 迭代策略，首先，根据不同的课程难度（kkk）进行迭代，
	# 在每一个难度的迭代里面，再根据每次向训练集中添加的实体对的个数是否大于阈值 θ２ 来判断是否继续迭代
	for kkk in [10, 6, 4,2,0]:
		ite_counter += 1
		output_layer, loss = build_SE(Config.se_dim, Config.act_func, Config.gamma, Config.k, e, train_array, KG1 + KG2)
		se_vec, J = training(output_layer, loss, 25, Config.epochs_se, train_array, e, Config.k)
		np.save(storepath + 'se_vec'+ str(ite_counter) + '.npy', se_vec)
		print('loss:', J)
		print('Result of SE:')
		outfile.write('Result of SE:\n')
		outfile.flush()
		index1, gap1, truths1, ranks1, index2, gap2, truths2, ranks2 = get_combine_hits_select_correct(se_vec, ne_vec, test, dicrank, len(test))
		trainlength_old = len(train)
		train, test, max_correct, dicrank = non_rep_match(test, train, index1, index2, gap1, gap2, ranks1, dicrank, id2fre, kkk)
		#train = sortbydegree(train)
		train_array = np.array(train) # array

		print('len of new train/seed: ' + str(len(train)))
		print('len of new test: ' + str(len(test)))
		print('len of max correct in the test: ' + str(max_correct))
		np.save(storepath + 'train'+ str(ite_counter) + '.npy', train)
		np.save(storepath + 'test'+ str(ite_counter) + '.npy', test)
		df2=open(storepath + 'dicrank'+ str(ite_counter) + '.npy','wb')
		pickle.dump(dicrank,df2)


		while len(train) - trainlength_old >= 20:
			ite_counter += 1
			output_layer, loss = build_SE(Config.se_dim, Config.act_func, Config.gamma, Config.k, e, train_array, KG1 + KG2)
			se_vec, J = training(output_layer, loss, 25, Config.epochs_se, train_array, e, Config.k)
			np.save(storepath + 'se_vec'+ str(ite_counter) + '.npy', se_vec)
			print('loss:', J)
			print('Result of SE:')
			outfile.write('Result of SE:\n')
			outfile.flush()
			index1, gap1, truths1, ranks1, index2, gap2, truths2, ranks2 = get_combine_hits_select_correct(se_vec, ne_vec, test, dicrank, len(test))
			trainlength_old = len(train)
			train, test, max_correct, dicrank = non_rep_match(test, train, index1, index2, gap1, gap2, ranks1, dicrank, id2fre, kkk)
			#train = sortbydegree(train)
			train_array = np.array(train) # array

			print('len of new train/seed: ' + str(len(train)))
			print('len of new test: ' + str(len(test)))
			print('len of max correct in the test: ' + str(max_correct))
			np.save(storepath + 'train'+ str(ite_counter) + '.npy', train)
			np.save(storepath + 'test'+ str(ite_counter) + '.npy', test)

			df2=open(storepath + 'dicrank'+ str(ite_counter) + '.npy','wb')
			pickle.dump(dicrank,df2)

		print('End of '+  str(kkk))








