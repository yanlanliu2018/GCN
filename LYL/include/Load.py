import pickle

import numpy as np
# load a file and return a list of tuple containing $num integers in each line
def loadfile(fn, num=1):
	print('loading a file...' + fn)
	ret = []
	with open(fn, encoding='utf-8') as f:
		for line in f:
			th = line[:-1].split('\t')
			x = []
			for i in range(num):
				x.append(int(th[i]))
			ret.append(tuple(x))
	return ret


def get_ent2id(fns):
	ent2id = {}
	for fn in fns:
		with open(fn, 'r', encoding='utf-8') as f:
			for line in f:
				th = line[:-1].split('\t')
				ent2id[th[1]] = int(th[0])
	return ent2id

# 根据文件获取实体名的向量表示
def loadNe(path):
	f1 = open(path)
	vectors = []

	#对实体名向量进行序列化，序列化格式：{id:[name,name_cev]}
	with open(path, "rb+") as f:
	    d = pickle.load(f)

	for i in range(30000):
		vectors.append(d[i][1].tolist())

	embeddings = np.vstack(vectors) # 实体名的 vec 应该是按照id的顺序进行存储的
	# 按垂直方向（行顺序）堆叠数组构成一个新的数组
	# 也就是得到的新的矩阵：行-vectors.len，列-vect.len
	return embeddings

# 根据文件获取实体属性文本信息的向量表示
def loadAse(path):
	f1 = open(path)
	vectors = []

	#以EntityID：EntityAttrEmedding(字典)的格式存入文件
	#对实体名属性文本向量进行序列化，序列化格式：{id:attr_str_vec}
	with open(path, "rb+") as f:
	    d = pickle.load(f)

	for i in range(30000):
		vectors.append(d[str(i)].tolist())

	embeddings = np.vstack(vectors) # 实体名的 vec 应该是按照id的顺序进行存储的
	# 按垂直方向（行顺序）堆叠数组构成一个新的数组
	# 也就是得到的新的矩阵：行-vectors.len，列-vect.len
	return embeddings
