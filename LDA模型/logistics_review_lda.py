# -*- coding utf-8 -*-

from gensim import corpora, models, similarities
from all_word_frequency import load_stopwords
import pandas as pd
import jieba
import numpy as np
import time
from pprint import pprint



#使用jieba分词对物流有关评论进行分词,并写入目标文件,作为LDA模型的语料库
def segment():
    stopwords = load_stopwords()
    data = pd.read_csv('logistics_review.csv', header=0, encoding="gbk")
    text = []
    print("分词开始。。。。。。。")
    start_time = time.time()
    for index, info in enumerate(data['Info']):
        info_words = []
        for word in jieba.cut(info):
            if word not in stopwords:
                info_words.append(word)
        if info_words:
            words = " ".join(info_words)
        else:
            words = np.nan
        text.append(words)
    print("分词结束。。。。。。。")
    end_time = time.time()
    print("耗时：" + str(end_time - start_time) + "s")
    words_df= pd.DataFrame({"words":text})
    data = pd.concat([data[['time','score']], words_df], axis=1)
    data.dropna(axis=0, how='any', inplace=True)
    data.to_csv('logistics_review_words.csv', sep=',', header=True, index=False)



#训练LDA主题模型,得物流评论的主题分布及词分布

def lda():
    np.set_printoptions(linewidth=300)
    data = pd.read_csv('logistics_review_words.csv', header=0,encoding="gbk")
    texts = []
    for info in data['words']:
        texts.append(info.split(' '))
    M = len(texts)
    print('文档数目：%d个' % M)
    print('正在建立词典......')
    dictionary = corpora.Dictionary(texts)
    V = len(dictionary)
    print('正在计算文本向量......')
    corpus = [dictionary.doc2bow(text) for text in texts]
    print('正在计算文档TF-IDF......')
    t_start = time.time()
    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    print('建立文档TF-IDF完成，用时%.3f秒' % (time.time() - t_start))
    print('LDA模型拟合推断......')
    num_topics = 15
    t_start = time.time()
    lda = models.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary,
                            alpha=0.01, eta=0.01, minimum_probability=0.001,
                            update_every = 1, chunksize = 100, passes = 5)
    print(u'LDA模型完成，训练时间为\t%.3f秒' % (time.time() - t_start))
    # 所有文档的主题
    # doc_topic = [a for a in lda[corpus_tfidf]]
    # print('Document-Topic:\n')
    # pprint(doc_topic)
    num_show_term = 5  # 每个主题显示几个词
    print(u'每个主题的词分布：')
    for topic_id in range(num_topics):
        print(u'主题#%d：\t' % topic_id)
        term_distribute_all = lda.get_topic_terms(topicid=topic_id)
        term_distribute = term_distribute_all[:num_show_term]
        term_distribute = np.array(term_distribute)
        term_id = term_distribute[:, 0].astype(np.int)
        for t in term_id:
            print(dictionary.id2token[t])
        print(u'\n概率：\t', term_distribute[:, 1])
    # 随机打印某10个文档的主题
    np.set_printoptions(linewidth=200, suppress=True)
    num_show_topic = 5  # 每个文档显示前几个主题
    print( u'10个评论的主题分布：')
    doc_topics = lda.get_document_topics(corpus_tfidf)  # 所有文档的主题分布
    idx = np.arange(M)
    np.random.shuffle(idx)
    idx = idx[:10]
    for i in idx:
        topic = np.array(doc_topics[i])
        topic_distribute = np.array(topic[:, 1])
        # print topic_distribute
        topic_idx = topic_distribute.argsort()[:-num_show_topic - 1:-1]
        print((u'第%d个评论的前%d个主题：' % (i, num_show_topic)), topic_idx)
        print(topic_distribute[topic_idx])

if  __name__ == "__main__":
    # segment()
    lda()
    pass
