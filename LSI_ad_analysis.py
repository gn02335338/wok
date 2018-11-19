# -*- coding: utf-8 -*-
####
##分析廣告及文章標題之相關性
##
##Author    :Jack Tang
##Date      :2018-11-19
##version   :v1.0
####

from gensim import corpora,models,similarities,utils
import jieba
import jieba.posseg as pseg
import re
import datetime
import random
import pandas as pd
import gensim


#讀取廣告資料
ad_data_list = pd.read_csv('ad_data', header=None)


#讀取文章標題資料
news_data = pd.read_csv('all_news_title.csv', header=None)

#將廣告與文章的標題做成list
ad_title_list = []
for i in range(len(ad_data_list)):
    ad_title_list.append(ad_data_list[i][0])

news_title_list = []
for i in range(len(news_data[0])):
    news_title_list.append(news_data[0][i])


#停用字
with open('/Users/jack/Desktop/LDA/stopword.txt', encoding='utf-8') as f:
    stop_word_list = f.readlines()
    
stop_word_list = [x.strip() for x in stop_word_list]

#LSI
lsi_sims_result = []
for index in range(len(news_title_list)):
    texts_list = []
    ad_title_list.append(news_title_list[index])
    for i in ad_title_list:
        tokens = jieba.cut(i,cut_all=False,HMM=True)
        stopped_tokens = [i for i in tokens if not i in stop_word_list]
        texts_list.append(stopped_tokens)
        
    ad_title_list = ad_title_list[:-1]
    

    # 重建tfidf model
    dictionary = corpora.Dictionary(texts_list)
    corpus = [dictionary.doc2bow(text) for text in texts_list]
    tfidfModel = models.TfidfModel(corpus)
    # 轉為向量表示
    tfidfVectors = tfidfModel[corpus]
    
    #建立lsi model
    lsi_model = models.LsiModel(tfidfVectors, id2word=dictionary, num_topics=5)
    

    #corpus_lsi = lda_model.get_document_topics(tfidfVectors ,minimum_probability=0)
    # 建立索引
    #indexLDA = similarities.MatrixSimilarity(ldamodel[tfidfVectors])
    indexLSI = similarities.MatrixSimilarity(lsi_model[corpus])
    
    sims = indexLSI[lsi_model[dictionary.doc2bow(texts for texts in news_title_list[index])]]
    #不排序方便後續操作
#   sims = sorted(enumerate(sims), key=lambda item: -item[1])
#   print(index ,sims)
    lsi_sims_result.append(sims)

sims_result_sort = []
for index in range(len(ad_data_list)):
	ad_sims = []
	for i in range(len(lsi_sims_result)):
		ad_sim = [i, lsi_sims_result[i][index]]
		ad_sims.append(ad_sim)
	#相關性排序
	ad_sims = sorted(ad_sims, key=lambda x: x[1], reverse=True)
	#print 相關性前十
	print('廣告標題: ',ad_data_list[index])
	for i in range(10):
	    print(i+1, news_title_list[ad_sims[i][0]],ad_sims[i][1])















