# -*- coding utf-8 -*-

import pandas as pd
import jieba
import time




#加载停用词文件返回停用词列表

def load_stopwords():
    f_stop = open('stop_words.txt', encoding="gbk")
    try:
        sw = [line.strip() for line in f_stop]
    finally:
        f_stop.close()
    return sw



#采用jieba分词,将每一条进行分词,并统计出来全量词汇的词频，降序排序，写入目标文件

def word_count():
    stopwords = load_stopwords()
    data = pd.read_csv('all_reviews_clean.csv', header=0,encoding="gbk")
    word_dict = {}
    print("词频统计开始。。。。。。。")
    start_time = time.time()
    for info in data['Info']:
        for word in jieba.cut(info):
            if word not in stopwords:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                   #字典中如果不存在键，就加入键，键值设置为1
                    word_dict[word] = 1
    print("词频统计结束。。。。。。。")
    end_time = time.time()
    print("耗时："+str(end_time-start_time)+"s")
    #按照词频降序排序
    word_dict = sorted(word_dict.items(), key=lambda item:item[1], reverse=True)
    #统计结果写入目标文件
    with open("all_word_frequency.txt","w") as f:
        for key,value in word_dict:
            f.write(key+"  "+str(value)+"\n")

if __name__ == "__main__":
    word_count()