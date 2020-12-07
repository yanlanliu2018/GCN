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

def loadNe(path):
	f1 = open(path)
	vectors = []
	# enumerate(): 将可遍历对象组合为一个索引序列，同时列出数据和数据下标
	for i, line in enumerate(f1):
		id, word, vect = line.rstrip().split('\t', 2)
		# 删除尾部空格，并以'\t'为分割符，将字符串分割为3段
		# id：实体id，word：实体名，vect：实体名的向量表示

		vect = np.fromstring(vect, sep=' ') # 将字符串以' '为分隔符构造矩阵，即词向量
		vectors.append(vect)
	embeddings = np.vstack(vectors) # 实体名的 vec 应该是按照id的顺序进行存储的
	# 按垂直方向（行顺序）堆叠数组构成一个新的数组
	# 也就是得到的新的矩阵：行-vectors.len，列-vect.len
	return embeddings
