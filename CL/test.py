# map = {'n':1,'j':2}
# for r in map:
#     print(r)

# e = 10
# du = [1] * e
# print(du)
import math
import tensorflow as tf
ind = [[0, 0], [1, 2]]
val = [1, 2]
den = [3,4]
M = tf.SparseTensor(indices=ind, values=val, dense_shape=den)
print(M)