# -*- coding: utf-8 -*-









import requests
import time
import pymysql
import datetime
import json
import configparser
import zmq
import gensim
from gensim import corpora, models, similarities
from bs4 import BeautifulSoup
from cate_doc_system_mysql import write_log
from cate_doc_system_mysql import lda_proba
from cate_doc_system_mysql import logistic_model
from cate_doc_system_mysql import load_xydata


# load system config
sys_config = configparser.ConfigParser()
sys_config.read('/config/sysconfig.ini')

master_image_api = sys_config.get('master_api','image_api')
master_push_api  = sys_config.get('master_api','image_api')
pigeon_push_api  = sys_config.get('pigeon_api','send_puah_api')
######
crm_push_api     = sys_config.get('crm_api','web_notification_api')
zmq_owl_host     = sys_config.get('zmq_owl','host')
zmq_owl_pop_port = sys_config.get('zmq_owl','pop_port')
######
pigeon_host      = sys_config.get('zmq_pigeon','host')
pigeon_port      = sys_config.get('zmq_pigeon','port')

def connect_mysql(server_name, db_name):
	# set parameter
	host     = sys_config.get(server_name, 'localhost')
	account  = sys_config.get(server_name, 'user')
	password = sys_config.get(server_name, 'passwd')

	# connect database
	db = pymysql.connect(host, account, password, db_name, charset = 'utf8')
	return db

def get_ad_data():


	return ad_data_list


def get_news_from_owl()


def gensim_news_and_ad()

	# jieba setting
	lda_proba.warm_jieba()

	# start listening
	print('listening...')

	# get msg
	msg = socket.recv()

	# 計時開始
	tStart = time.time()

	# connect database
	db_report = url_index.connect_mysql_report()
	db 	      = url_index.connect_mysql()

	# get th newest keyword group
	all_key   = popular_doc_by_time.get_newest_keyword(db)
	print('Key words:' + str(all_key))

	# json for msg
	msg = msg.decode('utf-8')
	msg = json.loads(msg)
	write_log.write_log('接收資料：' + str(msg), 'LDA', 1)

	# recall received
	socket.send_string('received')

	# set received msg
	data_title     = msg['title']
	data_time      = datetime.datetime.strptime(msg['time_now'],'%Y-%m-%d %H:%M:%S')
	data_context   = msg['paragraph']
	data_url       = msg['url']
	data_img       = msg['img_id']
	data_keyword   = msg['key_words']
	data_news_time = msg['news_time']
	web_id 		   = msg['web_id']
	category_id    = msg['category_id']

	#廣告資料

	

	# ad_title 	   = ad_msg[i]['title']
	# ad_time	       = datetime.datetime.strptime(ad_msg['time_now'],'%Y-%m-%d %H:%M:%S')
	# ad_context     = ad_msg[i]['paragraph']
	# ad_url         = ad_msg[i]['url']
	# ad_img         = ad_msg[i]['img_id']
	# ad_keyword     = ad_msg[i]['key_words']
	# ad_need        = ad_msg[i]['ad_need']


	# load model
	dictionary = lda_proba.load_dict()	
	ldamodel   = lda_proba.load_model()

	# 把文章內容進行 jieba斷句和gensim分類
	#write_log.write_log('start jieba ', 'LDA',1)
	lda_jieba_doc    = lda_proba.jieba_doc(data_context)

	# 對廣告內容進行 jieba
	# lda_jiebd_doc_ad_list = []
	# for i in range(len(ad_list)):
	# 	jiebd_ad = lda_proba.jieba_doc(ad_list[i][1])
	# 	#文字前面放ad的index
	# 	lda_jiebd_doc_ad_list.append([ad_list[i][0], jiebd_ad])

	# 是否推播 檢查之前是否推過
	#is_push = check_pushed.check_pushed(db_report, web_id, category_id, data_url, data_title)
	#db_report.close()
	#write_log.write_log('check_pushed:' + str(is_push), 'LDA', 1)
		

	#write_log.write_log('start lda ', 'LDA',1)
	# if web_id == 'nownews':
	# 	jibea_index_doc = lda_proba.index_doc(lda_jieba_doc, dictionary_nownews)
	# 	lda_result, max_n_topic	= lda_proba.cate_doc_result(jibea_index_doc, ldamodel_nownews, 5)
	# else:
	# 	jibea_index_doc = lda_proba.index_doc(lda_jieba_doc, dictionary)
	# 	lda_result, max_n_topic	= lda_proba.cate_doc_result(jibea_index_doc, ldamodel, 5)

	#for 廣告
	# lda_result_ad_list = []
	# max_n_topic_ad_list = []
	# for i in range(len(ad_list)):
	# 	jibea_index_doc_ad = lda_proba.index_doc(lda_jiebd_doc_ad_list[i][1], dictionary)
	# 	lda_result_ad, max_n_topic_ad = lda_proba.cate_doc_result(jibea_index_doc_ad, ldamodel, 5)
	# 	lda_result_ad_list.append(lda_result_ad)
	# 	max_n_topic_ad.append(max_n_topic_ad)

	# update news_page db
		
	# if len(lda_result) > 0:

	# 	if data_img != 'no_image':
	# 		try:
	# 			news_page_special.main_process(title = data_title, content = data_context, url = data_url, image = data_img, web_id = web_id, news_time = data_news_time, lda_result = lda_result)
				
	# 		except:
	# 			print('news page update fail')
			
	# 	if is_push == 1:

	# 		# time variable into dummy variable
	# 		hit_time = group_by_time.group_by_day(data_time)[:-1]
	# 		hit_time.extend(group_by_time.group_by_week(data_time)[:-1])

	# 		# popular doc - selection standard

	# 		# # method 1 - Similarity
	# 		dis = popular_distance.popular_d(lda_result)
	# 		print('文章相似度：' + str(dis[1]))
	# 		write_log.write_log('文章相似度：'+str(dis[1]),'LDA')
	# 		#method 2 - popular keyword
	# 		cursor = db.cursor()	

	#相似度分析
	#以新聞作為比較基準
	# doc = lda_jieba_doc
	# vec_bow = dictionary.doc2bow(doc.split()) 
	# vec_lda = lda[vec_bow] 
	
	# #建立索引
	# index = similarities.MatrixSimilarity(lda[corpus]) 
	

	# # 計算相似度
	# ad_sims_list = index[vec_lda] 
	# ad_sims_list = sorted(enumerate(sims), key=lambda item: -item[1])

	#ad_sims_list形式:[(2, 0.99679214), (1, 0.87377143), (3, 0.84817392), (5, 0.67252529), (4, 0.66729981)]

	ad_context_list = []
	for i in range(len(ad_data_list)):
		ad_context_list.append(ad_data_list[i][1])
	

	ad_sims_list = lda_sims.news_ad_sims(lda_jieba_doc, ad_context_list)
	
	#整理為[ad_index, ad_id, ad_sims, ad_amount,lda_ad_result]
	ad_list = []
	for i in range(len(ad_sims_list)):
		ad_index = ad_sims_list[i][0]
		ad_id = ad_data[ad_index][1]
		ad_sims = ad_sims_list[i][1]
		ad_amount = ad_data[ad_index][2]
		lda_ad = da_result_ad_list[ad_index]
		ad_list.append([ad_index, ad_id, ad_sims, ad_amount, lda_ad])












def select_ad_to_user(db, user_list, ad_list):

#	cursor = db.cursor()
	
	
	need_ad_token_index = []


	#設定門檻值,超過門檻值進行第一次的配對
	threshold = 0.5

	select_ad_list = []
	not_select_ad_list = []


	for i in range(len(ad_list)):
		if ad_list[i][2] >= threshold:
			select_ad_list.append(ad_list[i])

		else:
			not_select_ad_list.append(ad_list[i])

	#排序相關性由高至低
	select_ad_list = sorted(select_ad_list, key=lambda x:x[2], reverse=True)

	#user = [token_id, user_model_train_over, user_model]	


	#打亂user排序
	random.shuffle(user_list)
	
	while select_ad_list != [] and user_list != []:
    	for select_ad in select_ad_list:
    		for user in user_list:
    			#判斷廣告是否還有額度
    			if select_ad[3] == 0:
    				select_ad_list.remove(select_ad)
    				break
    			else:
    				need_ad_token_index.append([user[0], select_ad[0], select_ad[2]])
    				select_ad[3] = int(select_ad[3]) - 1
    				user_list.remove(user)	





	#剩下的廣告對用戶做分析
	#lda_result_ad, max_n_topic = lda_proba.cate_doc_result(jibea_index_doc, ldamodel, n)

	

	#媒合剩餘廣告
	while user_list != [] and not_select_ad_list != []:
        for user in user_list:
            user_model_train_over = int(user[1])
            if user_model_train_over == 1:

                for re_select_ad in not_select_ad_list:
                    re_select_ad_result = []
                    #判斷廣告是否還有額度
                    if re_select_ad[3] == 0:
                        not_select_ad_list.remove(re_select_ad)
                    else:        
                        user_model = [float(coef_i) for coef_i in user[2].split(',')]
                        yhat = logistic_model.predicted_hit(re_select_ad[4], hit_time, user_model)
                        re_select_ad_result.append([re_select[0], yhat, re_select[2]])
                #排序廣告與User之相關性
                re_select_ad_result = sorted(re_select_ad_result, key=lambda x:x[1], reverse=True)
                best_select_ad = re_select_ad_result[0]
                need_ad_token_index.append(user[0], best_select_ad[0])
                not_select_ad_list[best_select_ad][3] = int(not_select_ad_list[best_select_ad][3]) - 1
                user_list.remove(user)            
            
            #若沒有模型則隨機挑選廣告給User
            else:
                random_select_ad = random.choice(not_select_ad_list)
                #判斷廣告是否還有額度
                if random_select_ad[3] == 0:
                    not_select_ad_list.remove(random_select_ad)
                    #重新隨機選擇廣告
                    random_select_ad = random.choice(not_select_ad_list)
                else:
                    need_ad_token_index.append([user[0], random_select_ad[0], random_select_ad[2]])
                    random_select_ad[3] = int(random_select_ad[3]) - 1
                    user_list.remove(user)
	



	return 


# def send_data_to_server(msg_send, ip_address, port_address):
# 	try:
# 		# create client connection
# 		context = zmq.Context()
# 		socket = context.socket(zmq.REQ)

# 		# set wait how long need to clear waiting data
# 		socket.setsockopt(zmq.LINGER, 25000) # 25.000 sec
# 		# connect to server 
# 		socket.connect('tcp://%s:%s'%(ip_address,port_address))
# 		# set wait time out (ms)
# 		socket.RCVTIMEO = 25000 # 25 sec
# 		# message and uft-8 encode
# 		msg_send = msg_send.encode('utf-8')

# 		# send data to server and get back result
# 		socket.send(msg_send)
# 		msg_recv = socket.recv()

# 		return msg_recv

# 	except Exception as error:
# 		write_log(str(error))


if __name__ == '__main__':








