# -*- coding: utf-8 -*-
####
##第一階段標題相關性分析，相關性=1者進入第二階段內容相關性分析
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
#廣告格式[ad_title, ad_context]
ad_data_list = pd.read_csv('ad_data.csv', header=None)


#讀取文章資料
#文章格式[news_title, news_context]
news_data = pd.read_csv('all_news_title.csv', header=None)

#將廣告與文章的標題做成list
ad_title_list = []
for i in range(len(ad_data_list)):
    ad_title_list.append(str(ad_data_list[i][0]))

news_title_list = []
for i in range(len(news_data[0])):
    news_title_list.append(str(news_data[0][i]))


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
    lsi_model = models.LsiModel(tfidfVectors, id2word=dictionary, num_topics=2)

    # 建立索引
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

	#計算相關性為1之個數
    sims_result_count = []
    for i in range(len(ad_sims)):
        if int(ad_sims[i][1]) >= 1:
            sims_result_count.append(ad_sims)
    #print 相關性為1之標題
    print('廣告標題: ',ad_data_list[index][0])
    index_list = []
    for i in range(len(sims_result_count)):
        print(i+1, news_title_list[ad_sims[i][0]],ad_sims[i][1])
        index_list.append(ad_sims[i][0])

	#print 相關性前十
	print('廣告標題: ',ad_data_list[index][0])
	#記錄前十名文章之index
	index_list = []
	for i in range(10):
	    print(i+1, news_title_list[ad_sims[i][0]],ad_sims[i][1])
	    index_list.append(ad_sims[i][0])

	print('------------------------------------------------------------------------------------------------------------')
	#進入第二階段文章內容相關性分析

	# 標題相關性前十文章之內文
	news_context_list = []
	for i in index_list:
	    news_context_list.append(str(news_data[1][i]))
	# 廣告內文    
	ad_context_list = [str(ad_data_list[index][1])]

	#LSI
	context_lsi_sims_result = []
	for index in range(len(news_context_list)):
	    texts_list = []
	    ad_context_list.append(news_context_list[index])
	    for i in ad_context_list:
	        tokens = jieba.cut(i,cut_all=False,HMM=True)
	        stopped_tokens = [i for i in tokens if not i in stop_word_list]
	        texts_list.append(stopped_tokens)

	    ad_context_list = ad_context_list[:-1]


	    # tfidf model
	    dictionary = corpora.Dictionary(texts_list)
	    corpus = [dictionary.doc2bow(text) for text in texts_list]
	    tfidfModel = models.TfidfModel(corpus)
	    # 轉為向量表示
	    tfidfVectors = tfidfModel[corpus]

	    #建立lsi model
	    lsi_model = models.LsiModel(tfidfVectors, id2word=dictionary, num_topics=2)

	    # 建立索引
	    indexLSI = similarities.MatrixSimilarity(lsi_model[corpus])

	    # 相關性
	    sims = indexLSI[lsi_model[dictionary.doc2bow(texts for texts in news_context_list[index])]]
	    context_lsi_sims_result.append(sims)

	context_sims_result_sort = []
	
    ad_sims = []
    for i in range(len(context_lsi_sims_result)):
        ad_sim = [i, context_lsi_sims_result[i][0]]
        ad_sims.append(ad_sim)
    #相關性排序
    ad_sims = sorted(ad_sims, key=lambda x: x[1], reverse=True)
    context_sims_result_sort.append(ad_sims)
    #print 相關性前10
    print('廣告標題: ',ad_data_list[index][0])
    print('廣告內容: ',ad_data_list[index][1])
    for i in range(min(10,len(index_list))):
        print(i+1, news_data[0][index_list[ad_sims[i][0]]], ad_sims[i][1], ad_sims[i][0])
        print(news_context_list[ad_sims[i][0]])


















