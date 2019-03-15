#-*- coding:utf-8 -*-

import pandas as pd


#加载物流评论关键词返回物流评论关键词
def load_logistics_words():
    data = open('logistics_keywords_dict.txt',encoding="utf-8")
    try:
        logistics_keywords = [word.strip() for word in data]
    finally:
        data.close()
    return logistics_keywords



#根据物流关键词,筛选出有关物流的评论,并将结果写入到目标文件中
def logistics_review_filter():
    logistics_keywords = load_logistics_words()
    data = pd.read_csv('all_reviews_clean.csv', header=0, encoding="gbk")
    index_list = []
    for index, info in enumerate(data['Info']):
        for word in logistics_keywords:
            if word in info:
                index_list.append(index)
                break
    data = data.iloc[index_list]
    print(data.shape)
    data.to_csv('logistics_review.csv', sep=',',header=True, index=False)



#将筛选出来的物流评论,按照季度进行分割(2016,2017共计八个季度)
def logistics_review_cut():
    data = pd.read_csv('logistics_review.csv', header=0, encoding="gbk")
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
    data.iloc[index_list_201601].to_csv('cut_data/logistics_review_201601.csv', sep=',',header=True, index=False)
    data.iloc[index_list_201602].to_csv('cut_data/logistics_review_201602.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201603].to_csv('cut_data/logistics_review_201603.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201604].to_csv('cut_data/logistics_review_201604.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201701].to_csv('cut_data/logistics_review_201701.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201702].to_csv('cut_data/logistics_review_201702.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201703].to_csv('cut_data/logistics_review_201703.csv', sep=',', header=True, index=False)
    data.iloc[index_list_201704].to_csv('cut_data/logistics_review_201704.csv', sep=',', header=True, index=False)

if __name__ == "__main__":
    #print(load_logistics_words())
    logistics_review_filter()
    #logistics_review_cut()
    pass