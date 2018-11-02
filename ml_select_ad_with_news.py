# -*- coding: utf-8 -*-









import requests
import time
import pymysql
import datetime
import json
import configparser
import zmq
import gensim
from cate_doc_system_mysql import write_log

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

def get_data_from_owl()

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

	# load model
	dictionary, dictionary_nownews = lda_proba.load_dict()	
	ldamodel, ldamodel_nownews     = lda_proba.load_model()

	# 把文章內容進行 jieba斷句和gensim分類
	write_log.write_log('start jieba ', 'LDA',1)
	lda_jieba_doc   = lda_proba.jieba_doc(data_context)
		

	write_log.write_log('start lda ', 'LDA',1)
	if web_id == 'nownews':
		jibea_index_doc = lda_proba.index_doc(lda_jieba_doc, dictionary_nownews)
		lda_result, max_n_topic	= lda_proba.cate_doc_result(jibea_index_doc, ldamodel_nownews, 5)
	else:
		jibea_index_doc = lda_proba.index_doc(lda_jieba_doc, dictionary)
		lda_result, max_n_topic	= lda_proba.cate_doc_result(jibea_index_doc, ldamodel, 5)

	# update news_page db
		
	if len(lda_result) > 0:

		if data_img != 'no_image':
			try:
				news_page_special.main_process(title = data_title, content = data_context, url = data_url, image = data_img, web_id = web_id, news_time = data_news_time, lda_result = lda_result)
				
			except:
				print('news page update fail')
			
		if is_push == 1:

			# time variable into dummy variable
			hit_time = group_by_time.group_by_day(data_time)[:-1]
			hit_time.extend(group_by_time.group_by_week(data_time)[:-1])

			# popular doc - selection standard

			# # method 1 - Similarity
			# dis = popular_distance.popular_d(lda_result)
			# print('文章相似度：' + str(dis[1]))
			# write_log.write_log('文章相似度：'+str(dis[1]),'LDA')
			# method 2 - popular keyword
			cursor = db.cursor()






def get_ad_data():


	return ad_data_list


def select_ad_to_user(db,):
	cursor = db.cursor()

	sql = '''SELECT''' 

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



	return 
def ad_







