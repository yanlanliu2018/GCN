#！/usr/bin/env python
#-*-coding:utf-8-*-
nameId = int('3')
print(nameId)

s = "0	http://dbpedia.org/resource/Jannie_du_Plessis"
lines = s.split('\t')
nameString = lines[1].split('/')[-1]
nameId = int(lines[0])
print(nameId)
print(nameString)

for i in range(len(lines)):
    print(i)