

from LYL.code.support.Config import Config

# 获取所有实体的实体名及其向量表示，
# 以EntityID\tEntityName\tEntityEmedding(空格隔开)的格式存入文件
def get_name_string():
    # 获取G1的实体id和实体名
    path1 = './data/' + Config.language + '/mapping/0_3/triples_1'