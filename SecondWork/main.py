# encoding=utf-8
import jieba
import re
from decimal import Decimal
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math

# 获取指定路径的文件内容
def get_file_contents(path):
    str = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str

# 过滤得到词组集合
def filter(str):
    str = jieba.lcut(str)
    result = []
    for tags in str:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tags)): # 只保留字母与数字与所有中文
            result.append(tags)
        else:
            pass
    return result

# 得到所有词组组合
def get_all_words(list_a,list_b):
    all_words=[]
    for i in list_a:
        if(i not in all_words):
            all_words.append(i)
    for j in list_b:
        if(j not in all_words):
            all_words.append(j)
    return all_words

# 词频向量化
def get_word_vector(list_a,list_b,all_words):
    la=[]
    lb=[]
    for word in all_words:
        la.append(list_a.count(word))
        lb.append(list_b.count(word))
    return la,lb
# 计算余弦值，利用了numpy中的线代计算方法
def calculate_cos(la,lb):
    list_a_fin=np.array(la)
    list_b_fin=np.array(lb)
    cos=(np.dot(list_a_fin,list_b_fin.T))/((math.sqrt(np.dot(list_a_fin,list_a_fin.T)))*(math.sqrt(np.dot(list_b_fin,list_b_fin.T))))
    return cos

# 第二种方法 利用接口求余弦相似度
# sklearn中的sklearn.metrics.pairwise.cosine_similarity函数直接计算余弦相似度
def duplicate(num1, num2):
    num1 = np.array(num1)
    num2 = np.array(num2)
    result = cosine_similarity(num1.reshape(1, -1), num2.reshape(1, -1))[0][0]
    return result

if __name__ == '__main__':
    print('please enter the path of the origin work:')
    path1=input()
    print('please enter the path of the test work:')
    path2=input()
    print('please enter the path of the savedata:')
    save_path=input()
    # path1 = "F:\learning\softwareengineering\测试文本\orig.txt"
    # path2 = "F:\learning\softwareengineering\测试文本\orig_0.8_add.txt"
    # save_path = "F:\learning\softwareengineering\测试文本\save.txt"
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    allWords=get_all_words(text1,text2)
    list_a,list_b=get_word_vector(text1,text2,allWords)
    similarity=calculate_cos(list_a,list_b)
    # similarity=duplicate(list_a,list_b)
    print("文章相似度百分比： %.2f%%"%float(similarity*100))
    print("文章相似度： %.2f"%float(similarity))
    # 将相似度结果写入指定文件
    f = open(save_path, 'w', encoding="utf-8")
    f.write("文章相似度百分比： %.2f%%\n"%float(similarity*100))
    f.write("文章相似度： %.2f"%float(similarity))
    f.close()
