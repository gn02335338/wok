# -*- coding: utf-8 -*-

from gensim import corpora,models,similarities,utils
import jieba
import jieba.posseg as pseg
import re

def news_ad_sims(news_context, ad_context_list):

	jieba.load_userdict("/Users/jack/Desktop/LDA/dict.txt.big")
	# 處理廣告資料
	# 移除括號內的內容
	remover1=re.compile(r"\（.*?\）")
	remover2=re.compile(r"\[.*?\]")
	remover3=re.compile(r"\〔.*?\〕")
	remover4=re.compile(r"\(.*?\)")

	for i in range(len(ad_context_list)):
	        ad_context_list[i]=remover1.sub("",ad_context_list[i])
	        ad_context_list[i]=remover2.sub("",ad_context_list[i])
	        ad_context_list[i]=remover3.sub("",ad_context_list[i])
	        ad_context_list[i]=remover4.sub("",ad_context_list[i])

	with open('/Users/jack/Desktop/LDA/stopword.txt', encoding='utf-8') as f:
    	stop_word_list = f.readlines()
    
	stop_word_list = [x.strip() for x in stop_word_list]

	texts = []
	for i in ad_context_list:
	    tokens = jieba.cut(i,cut_all=False,HMM=True)
	    stopped_tokens = [i for i in tokens if not i in stop_word_list]
	    texts.append(stopped_tokens)

	# load dictionary
	dictionary = corpora.Dictionary.load('/Users/jack/Desktop/LDA/allnews_dictionary.dict')
 
	# 建立語料庫
	corpus = [dictionary.doc2bow(text) for text in texts]

	# load tfidf model
	tfidfModel = models.tfidfmodel.TfidfModel.load("/Users/jack/Desktop/LDA/tfidf_model.tfidf")

	'''
	# 重建tfidf model
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	tfidfModel = models.TfidfModel(corpus)
	'''

	# 轉為向量表示
	tfidfVectors = tfidfModel[corpus]

	# load lda model
	ldamodel = models.ldamodel.LdaModel.load('/Users/jack/Desktop/LDA/allnews_LDA_model.lda')

	corpus_lda = ldamodel.get_document_topics(tfidfVectors ,minimum_probability=0)
	# 建立索引
	#indexLDA = similarities.MatrixSimilarity(ldamodel[tfidfVectors])
	indexLDA = similarities.MatrixSimilarity(corpus_lda)

	# 以新聞內容作為比較基準

	sims = indexLDA[ldamodel[dictionary.doc2bow(news_context.split())]]
	# 排列相似度由大至小
	ad_sims_list = sorted(enumerate(ad_sims_list), key=lambda item: -item[1])

	return ad_sims_list, corpus_lda
