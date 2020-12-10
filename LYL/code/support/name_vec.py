import json
from LYL.code.support.Config import Config
from LYL.code.support.bert_support import BertSupport


def get_name_strAndVec():
    '''
    获取所有实体的实体名及其向量表示，
    以EntityID\tEntityName\tEntityEmedding(空格隔开)的格式存入文件

    :return:
    '''

    id_name = dict() #用于存储实体信息，格式：{id:[name,name_cev]}

    # 获取G1的实体id和实体名、实体名向量
    path1 = '../../data/' + Config.language + '/mapping/0_3/ent_ids_1'
    file1 = open(path1, 'r', encoding='utf-8')

    print("现在开始获取" + path1 + "中实体名的向量表示。")

    # num：用来统计已经获取了几个实体名，每1000个实体名进行一次bert的调用
    num = 0
    namelist = [] #用来暂时存储实体名，满1000个后调用bert
    nameList = [] # 记录G1的所有实体名
    idList = [] # 记录G1 的所有实体ID
    vecList = []   # 记录 G1 所有实体名的向量表示
    for line in file1:
        # 0	http://dbpedia.org/resource/Bachir_Gemayel
        lines = line.split('\t')
        nameString = lines[1].split('/')[-1].split('\n')[0]
        nameId = int(lines[0])

        idList.append(nameId)
        namelist.append(nameString)

        num+=1
        if(num%1000 == 0):
            print("已经获取了" + num +"条数据的实体名向量。")
            nameList.append(namelist)
            vecList.append(BertSupport().word_list_vector(wordList=namelist))

            namelist = []

    for i in range(len(idList)):
        id_name[idList[i]] = [nameList[i],vecList[i]]

    print("文件-" + path1 + "-获取实体名向量结束！")

    # 获取G2的实体id和实体名、实体名向量
    path2 = '../../data/' + Config.language + '/mapping/0_3/ent_ids_2'
    file2 = open(path2, 'r', encoding='utf-8')

    print("现在开始获取" + path2 + "中实体名的向量表示。")

    # num：用来统计已经获取了几个实体名，每1000个实体名进行一次bert的调用
    num = 0
    namelist = []  # 用来暂时存储实体名，满1000个后调用bert
    nameList = []
    idList = []
    vecList = []

    if(Config.language == "dbp_wd_15k_V1"):
        # 获取实体（Q1615188）与实体名称的映射
        path3 = '../../data/' + Config.language + '/mapping/0_3/ent_string_2.json'
        entAndPro_name_2 = json.load(open(path3, encoding='utf-8'))

        for line in file2:
            # 10500	http://www.wikidata.org/entity/Q325033
            lines = line.split('\t')
            nameNum = lines[1].split('/')[-1].split('\n')[0]
            nameString = entAndPro_name_2[nameNum]
            nameId = int(lines[0])

            idList.append(nameId)
            namelist.append(nameString)

            num += 1
            if (num % 1000 == 0):
                print("已经获取了" + num + "条数据的实体名向量。")
                nameList.append(namelist)
                vecList.append(BertSupport().word_list_vector(wordList=namelist))

                namelist = []
    else:
        for line in file2:
            # 10500	Bachir_Gemayel
            lines = line.split('\t')
            nameString = lines[1].split('/')[-1].split('\n')[0]
            nameId = int(lines[0])

            idList.append(nameId)
            namelist.append(nameString)

            num += 1
            if (num % 1000 == 0):
                print("已经获取了" + num + "条数据的实体名向量。")
                nameList.append(namelist)
                vecList.append(BertSupport().word_list_vector(wordList=namelist))

                namelist = []

    for i in range(len(idList)):
        id_name[idList[i]] = [nameList[i], vecList[i]]

    print("文件-" + path1 + "-获取实体名向量结束！")

    print("对实体名向量进行序列化，序列化格式：{id:[name,name_cev]}")
    # 将获取到的实体名的向量表示以json文档的形式序列化
    file = '../../data/'+ Config.language + '/mapping/0_3/name_vec_cpm_3.json'
    with open(file, 'w', encoding='UTF-8') as f:
        json.dump(id_name, f, ensure_ascii=False)
    print("序列化结束！")


if __name__ == "__main__":
    get_name_strAndVec()

