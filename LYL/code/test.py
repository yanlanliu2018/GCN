#！/usr/bin/env python
#-*-coding:utf-8-*-
import json
import pickle

from LYL.code.support.bert_support import BertSupport
import numpy as np

d1 = dict()
d1['1'] = 1
d1['2'] = 2

d2 = dict()
d2['3'] = 3
d2['4'] = 4
d2['2'] = 2

d1.update(d2)

print(d1)
print(d1.__len__())