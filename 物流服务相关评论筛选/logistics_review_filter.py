# -*- coding utf-8 -*-

import pandas as pd


#筛选物流评论,通过LDA聚类后主题模型的关键词,筛选出物流有关的主题,通过主题筛选物流有关评论


if __name__ == "__main__":
    data = pd.read_csv('logistics_review_topic.csv', header=0, encoding="gbk")
    data = data[(data["topic"].isin([2,3,11,13,14,15,16]))]
    index = []
    for i, words in enumerate(data['words']):
        # 评论中不重复词超过两个认为是有效物流评论
        if len(set(words.split(" "))) > 2:
            index.append(i)
    data = data.iloc[index]
    print(data.shape)
    data.to_csv('logistics_review_filter.csv', sep=',', header=True, index=False)