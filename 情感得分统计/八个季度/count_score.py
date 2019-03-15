# -*- coding utf-8 -*-

import pandas as pd
import os

def count_score():
    '''
    统计每句话下的指标关键词出现的次数
    :return:
    '''
    keywords_df = pd.read_csv('keywords.csv', header=0, sep=',')
    logistics_review_df = pd.read_csv('logistics_review.csv', header=0, sep=',', encoding="gbk")
    for index_re, info in enumerate(logistics_review_df["Info"]):
        kv = {}
        for index, words in enumerate(keywords_df["words"]):
            count = 0
            key = keywords_df.loc[index, 'key']
            for word in str(words).split(" "):
                if word in info:
                    count += 1
            kv[key] = count
        for key, value in kv.items():
            logistics_review_df.loc[index_re, key] = value
    logistics_review_df.drop('Info', axis=1, inplace=True)
    logistics_review_df.to_csv('review_score.csv', sep=',', header=True, index=False, encoding="utf-8")

def review_cut():
    '''
    将筛选出来的物流评论,按照季度进行分割(2016,2017共计八个季度)
    :return:
    '''
    data = pd.read_csv('review_score.csv', header=0)
    index_list_201601 = []
    index_list_201602 = []
    index_list_201603 = []
    index_list_201604 = []
    index_list_201701 = []
    index_list_201702 = []
    index_list_201703 = []
    index_list_201704 = []
    for index, info in enumerate(data['time']):
        time = info.split("/")
        year,month = time[0],time[1]
        if month.startswith("0") and len(month) == 2:
            month = month.replace("0","")
        if year == "2016" :
            if month =="1" or month =="2" or month =="3":
                index_list_201601.append(index)
            elif month =="4" or month =="5" or month =="6":
                index_list_201602.append(index)
            elif month =="7" or month =="8" or month =="9":
                index_list_201603.append(index)
            elif month =="10" or month =="11" or month =="12" :
                index_list_201604.append(index)
        elif year == "2017" :
            if month =="1" or month =="2" or month =="3":
                index_list_201701.append(index)
            elif month =="4" or month =="5" or month =="6":
                index_list_201702.append(index)
            elif month =="7" or month =="8" or month =="9":
                index_list_201703.append(index)
            elif month =="10" or month =="11" or month =="12" :
                index_list_201704.append(index)
    data.iloc[index_list_201601].to_csv('cut_data/review_score_201601.csv', sep=',',header=True, index=False)
    data.iloc[index_list_201602].to_csv('cut_data/review_score_201602.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201603].to_csv('cut_data/review_score_201603.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201604].to_csv('cut_data/review_score_201604.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201701].to_csv('cut_data/review_score_201701.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201702].to_csv('cut_data/review_score_201702.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201703].to_csv('cut_data/review_score_201703.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201704].to_csv('cut_data/review_score_201704.csv', sep=',', header=True, index=False)

def calc_score(input_file,out_file):
    '''
    计算各项指标,包括均值,标准差等,并保存到目标文件
    :param input_file: 输入文件
    :param out_file: 输出文件
    :return:
    '''
    score_df = pd.read_csv(input_file, header=0, sep=',')
    kv_sum = {}
    for i in range(1,17):
        kv = {}
        key="key"+str(i)
        data = score_df[["score",key]]
        data["sum"] = data["score"]*data[key]
        result = data.sum()
        num = int(result[1])
        kv["num"] = num
        mean = 0.0
        std = 0.0
        if num != 0:
            mean = result[2] / num
            sum = 0
            for index in range(len(data)):
                score = data.loc[index, "score"]
                index_sig= int(data.loc[index, key])
                # 验证数据准确性
                # if(index_sig != 0):
                #     print("------------")
                #     print(key)
                #     print(index)
                #     print(score)
                #     print(index_sig)
                sum += (((score - mean) ** 2)*index_sig)
            std = (sum / num) ** 0.5
        mean = float('%.4f' % mean)
        std = float('%.4f' % std)
        if len(str(mean)) != 4:
            kv["mean"] = str(mean)+"0"
        else:
            kv["mean"] = str(mean)
        if len(str(std)) != 4:
            kv["std"] = str(std)+"0"
        else:
            kv["std"] = str(std)
        kv_sum[key] = kv
    with open(out_file, "w",encoding="utf-8") as f:
        f.write("key,num,mean,std\n")
        for k1,v1 in kv_sum.items():
                f.write(k1+","+str(v1["num"])+","+v1["mean"]+","+v1["std"]+"\n")

def save_file():
    for root,dirs,files in os.walk("cut_data"):
        for filename in files:
            input_file = "cut_data/"+filename
            output_file = "score_data/count_score_"+filename[-10:]
            calc_score(input_file, output_file)

if __name__ == "__main__":
    count_score()
    review_cut()
    save_file()
    pass