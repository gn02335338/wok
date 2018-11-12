# -*- coding: utf-8 -*-







config = configparser.ConfigParser()
config.read('/config/sysconfig.ini')


# zmq for get lr data 
zmq_pangolin_host = sys_config.get('zmq_pangolin','host')
zmq_pangolin_port = sys_config.get('zmq_pangolin','get_token_from_lr_port')

# create zmq connect object
context = zmq.Context()
socket  = context.socket(zmq.REP)

# from LR system get 
socket.bind('tcp://' + zmq_pangolin_host + ':' + zmq_pangolin_port)


while True:

	# get msg
	msg = socket.recv()

	# 計時開始
	# tStart = time.time()

	# connect database
	db_report = url_index.connect_mysql_report()
	db 	      = url_index.connect_mysql()


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
	data_token     = msg['token']

	#廣告資料
	ad_data_list = []

	for ad_id_i in ad_id_list:
		ad_data = ml_select_ad_with_news.get_ad_data(db, ad_id_i)
		ad_data_list.append(ad_data)

	#點擊時間
	hit_time = datetime.datetime.now()


	# 把文章內容進行 jieba斷句
	#write_log.write_log('start jieba ', 'LDA',1)
	lda_jieba_doc    = lda_proba.jieba_doc(data_context)

	ad_context_list = []
	for i in range(len(ad_data_list)):
		ad_context_list.append(ad_data_list[i][1])

	# 文章內容與廣告進行相似度分析
	ad_sims_list, corpus_lda = lda_sims.news_ad_sims(lda_jieba_doc, ad_context_list)
		
	#整理為[ad_index, ad_id, ad_sims, ad_amount, lda_ad_result, hit_time]
	ad_list = []
	for i in range(len(ad_sims_list)):
		ad_index = ad_sims_list[i][0]
		ad_id = ad_data[ad_index][1]
		ad_sims = ad_sims_list[i][1]
		ad_amount = ad_data[ad_index][2]
		lda_ad = corpus_lda[ad_index]
		ad_list.append([ad_index, ad_id, ad_sims, ad_amount, lda_ad, hit_time])


	cursor = db.cursor()

	# get all user
	user_list = select_user.select_user(db,
		limit_by_day, 
		limit_by_hour, 
		limit_by_mom, 
		web_id,
		category_id,
		unconditional_breadcasting_switch)

	# [token_id, user_model_train_over, user_model]
	# 轉為dict = {token : model} 形式
	# token_list = []
	# model_list = []
	# for i in range(len(user_list)):
	# 	token_list.append(user_list[i][0])
	# 	model_list.append(user_list[i][2])
    
	# dict_token_model = dict(zip(token_list, model_list))

	dict_token_model = {}
	for user in user_list:
		dict_token_model[user[0]] = user[2]

	ad_user_list = []
	for token in data_token:
		ad_user_list.append([token, dict_token_model[token]])


	cursor.close()

	payload = ml_select_ad_with_news.select_ad_to_user(ad_user_list, ad_list)



	# if news_page_special.whether_attach_landing_page(web_id) and web_id in ['some web id']:

	# 	to_likr_dict = {'url':data_url,
	# 					'title':new_data_title,
	# 					'token':new_user_list,
	# 					'paragraph':new_data_context,
	# 					'amount':str(len(this_push_tokens)),
	# 					'img_id':data_img,
	# 					'web_id':web_id,
	# 					'category_id':category_id,
	# 					'cust_push_id':str(max_url_id),
	# 					'renotify_tag':str((max_url_id  % renotify_tag_number) + 1),
	# 					'icon':msg['icon'],
	# 					'btn_1_title':'猜你喜歡的新聞',
	# 					'btn_1_icon':'_',
	# 					'btn_1_url':landing_page_list[web_id],
	# 					'btn_2_title':'_',
	# 					'btn_2_icon':'_',
	# 					'btn_2_url':'_'
	# 					}
	# else:

	# 	to_likr_dict = {'url':data_url,
	# 					'title':new_data_title,
	# 					'token':new_user_list,
	# 					'paragraph':new_data_context,
	# 					'amount':str(len(this_push_tokens)),
	# 					'img_id':data_img,
	# 					'web_id':web_id,
	# 					'category_id':category_id,
	# 					'cust_push_id':str(max_url_id),
	# 					'renotify_tag':str((max_url_id  % renotify_tag_number) + 1),
	# 					'icon':msg['icon'],
	# 					'btn_1_title':'關注',
	# 					'btn_1_icon':'_',
	# 					'btn_1_url':'close',
	# 					'btn_2_title':'不喜歡',
	# 					'btn_2_icon':'_',
	# 					'btn_2_url':'close'
	# 					}
	# else:

	# 	to_likr_dict = {'url':data_url,
	# 					'title':new_data_title,
	# 					'token':new_user_list,
	# 					'paragraph':new_data_context,
	# 					'amount':str(len(this_push_tokens)),
	# 					'img_id':data_img,
	# 					'web_id':web_id,
	# 					'category_id':category_id,
	# 					'cust_push_id':str(max_url_id),
	# 					'renotify_tag':str((max_url_id  % renotify_tag_number) + 1),
	# 					'icon':msg['icon'],
	# 					'btn_1_title':'關注',
	# 					'btn_1_icon':'_',
	# 					'btn_1_url':'close',
	# 					'btn_2_title':'不喜歡',
	# 					'btn_2_icon':'_',
	# 					'btn_2_url':'close'
	# 					}


	# show_dict    = {'amount':str(len(this_push_tokens)),
	# 				'category_id':category_id,
	# 				'cust_push_id':str(max_url_id),
	# 				'renotify_tag':str((max_url_id  % renotify_tag_number) + 1)
	# 				}
						
	print(show_dict)









	#傳資料給pangolin
	server_feedback   = send_data_to_server(payload,'tcp://' + zmq_pangolin_host + ':' + zmq_pangolin_port)













