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

	for i in range(len(ad_list)):

	ad_title 	   = ad_msg[i]['title']
	ad_time	       = datetime.datetime.strptime(ad_msg['time_now'],'%Y-%m-%d %H:%M:%S')
	ad_context     = ad_msg[i]['paragraph']
	ad_url         = ad_msg[i]['url']
	ad_img         = ad_msg[i]['img_id']
	ad_keyword     = ad_msg[i]['key_words']
	ad_need        = ad_msg[i]['ad_need']


	# load model
	dictionary, dictionary_nownews = lda_proba.load_dict()	
	ldamodel, ldamodel_nownews     = lda_proba.load_model()

	# 把文章內容進行 jieba斷句和gensim分類
	write_log.write_log('start jieba ', 'LDA',1)
	lda_jieba_doc    = lda_proba.jieba_doc(data_context)

	lda_jiebd_doc_ad = lda_proba.jieba_doc(ad_context)

	# 是否推播 檢查之前是否推過
	#is_push = check_pushed.check_pushed(db_report, web_id, category_id, data_url, data_title)
	#db_report.close()
	#write_log.write_log('check_pushed:' + str(is_push), 'LDA', 1)
		

	write_log.write_log('start lda ', 'LDA',1)
	if web_id == 'nownews':
		jibea_index_doc = lda_proba.index_doc(lda_jieba_doc, dictionary_nownews)
		lda_result, max_n_topic	= lda_proba.cate_doc_result(jibea_index_doc, ldamodel_nownews, 5)
	else:
		jibea_index_doc = lda_proba.index_doc(lda_jieba_doc, dictionary)
		lda_result, max_n_topic	= lda_proba.cate_doc_result(jibea_index_doc, ldamodel, 5)

	#for 廣告
	jibea_index_doc_ad = lda_proba.index_doc(lda_jieba_doc_ad, dictionary)
	lda_result_ad, max_n_topic_ad = lda_proba.cate_doc_result(jibea_index_doc_ad, ldamodel, 5)

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
	doc = lda_jieba_doc
	vec_bow = dictionary.doc2bow(doc.split()) 
	vec_lda = lda[vec_bow] 
	print(vec_lda)








def select_ad_to_user(db,):

#	cursor = db.cursor()

#	sql = '''SELECT''' 

	#設定門檻值,超過門檻值才配送廣告
	threshold = 0.5

	select_ad_list = []
	not_select_ad_list = []

	for i in range(len(ads)):
		if ads[i][1] >= threshold:
			select_ad_list.append(ads[i])

		else:
			not_select_ad_list.append(ads[i])

	select_ad_list = sorted(select_ad_list, key=lambda x:x[1], reverse=True)

	ad_sim_index = 0
	for select_ad in select_ad_list:
		ad_data_list[select_ad_list[ad_sim_index][0]]


	#剩下的廣告對用戶做分析
	lda_result_ad, max_n_topic = lda_proba.cate_doc_result(jibea_index_doc, ldamodel, n)

	

	#媒合剩餘廣告
	for ad in not_select_ad_list:
		for user in user_list:
				token_id = user[0]
				user_model_train_over = int(user[1])

				if user_model_train_over == 1:
					user_model = [float(coef_i) for coef_i in user[2].split(',')]
					yhat = logistic_model.predicted_hit(lda_result_ad, hit_time, user_model)
					push_or_no = yhat_boundary(yhat, yhat_bdy)
					model_ok_count += 1
					if push_or_no == 1 :
						need_push_token_index.append((token_id, ad))
				else:
					random_selection_pool.append((token_id, ad))
	



	return 


def send_data_to_server(msg_send, ip_address, port_address):
	try:
		# create client connection
		context = zmq.Context()
		socket = context.socket(zmq.REQ)

		# set wait how long need to clear waiting data
		socket.setsockopt(zmq.LINGER, 25000) # 25.000 sec
		# connect to server 
		socket.connect('tcp://%s:%s'%(ip_address,port_address))
		# set wait time out (ms)
		socket.RCVTIMEO = 25000 # 25 sec
		# message and uft-8 encode
		msg_send = msg_send.encode('utf-8')

		# send data to server and get back result
		socket.send(msg_send)
		msg_recv = socket.recv()

		return msg_recv

	except Exception as error:
		write_log(str(error))


if __name__ == '__main__':








