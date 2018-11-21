# -*- coding: utf-8 -*-

import zmq
import json
import datetime
import configparser
import time
import os
from ml_push_web_api  import get_data_send_push
from cate_doc_system_mysql import url_index
from select_user import select_user


config = configparser.ConfigParser()
config.read('/config/sysconfig.ini')

def connect_mysql(server_name, db_name):
	# set parameter
	host     = sys_config.get(server_name, 'localhost')
	account  = sys_config.get(server_name, 'user')
	password = sys_config.get(server_name, 'passwd')

	# connect database
	db = pymysql.connect(host, account, password, db_name, charset = 'utf8')
	return db


while True:
	folder = os.walk('/home/work_place/wait_for_analyse_banner/')
	files = []

	for a,b,c in folder:
		for d in c:
			files.append(os.path.join(a,d))

	if len(files) > 0:

		# 打散新聞，不要同時一直推送同一個web_id
		#files = random.sample(files,len(files))

		for file in files:
			with open(file,'r',encoding='utf-8') as f:
				all_data= json.load(f)
			

			# set received msg
			data_url       = all_data['url']
			data_title     = all_data['title']
			data_token     = all_data['token']
			data_amount    = all_data['amount']
			data_context   = all_data['paragraph']
			data_img       = all_data['img_id']
			web_id 		   = all_data['web_id']
			category_id    = all_data['category_id']
			cust_push_id   = all_data['cust_push_id']
			renotify_tag   = all_data['renotify_tag']
			btn_1_title    = all_data['btn_1_title']
			btn_1_icon	   = all_data['btn_1_icon']
			btn_1_url	   = all_data['btn_1_url']
			btn_2_title    = all_data['btn_2_title']
			btn_2_icon     = all_data['btn_2_icon']
			btn_2_url      = all_data['btn_2_url']


			db = connect_mysql('db_owl', 'ML_user_data')			
			cursor = db.cursor()

			# sql query
			sql = "SELECT id, title, context, pre_clip, LDA1, LDA2 FROM AD WHERE pre_clip > 0 "
			cursor.execute(sql)
			ad_results = cursor.fetchall()
			#廣告資料
			ad_data_list = []
			for row in ad_results:
				ad_id = row[0]
				ad_title = row[1]
				ad_context = row[2]
				ad_amount = row[3]
				ad_lda1 = row[4]
				ad_lda2 = row[5]

				ad_data_list.append([ad_id, ad_title, ad_context, ad_amount, ad_lda1, ad_lda2])

			cursor.close()


			#點擊時間
			hit_time = datetime.datetime.now()


			# #取出廣告內容
			# ad_context_list = []
			# for i in range(len(ad_data_list)):
			# 	ad_context_list.append(str(ad_data_list[i][1]))

			#取出廣告標題
			ad_title_list = []
			for i in range(len(ad_data_list)):
				ad_title_list.append(str(ad_data_list[i][1]))


			#####
			LDA_function.prepare_jieba(file_path+"/jieba_material")
			# 處理廣告資料
			# 移除括號內的內容
			# remover1=re.compile(r"\（.*?\）")
			# remover2=re.compile(r"\[.*?\]")
			# remover3=re.compile(r"\〔.*?\〕")
			# remover4=re.compile(r"\(.*?\)")

			# data_context=remover1.sub("",data_context)
			# data_context=remover2.sub("",data_context)
			# data_context=remover3.sub("",data_context)
			# data_context=remover4.sub("",data_context)

			# for i in range(len(ad_context_list)):
			#         ad_context_list[i]=remover1.sub("",ad_context_list[i])
			#         ad_context_list[i]=remover2.sub("",ad_context_list[i])
			#         ad_context_list[i]=remover3.sub("",ad_context_list[i])
			#         ad_context_list[i]=remover4.sub("",ad_context_list[i])

			stop_word_list = LDA_function.load_stopword_list(file_path+"/jieba_material")

			# data_title_jieba = [LDA_function.jieba_sentence_segmentation(i, stopword_list) for i in data_title if i not in stopword_list]
			# ad_title_jieba = [LDA_function.jieba_sentence_segmentation(i, stopword_list) for i in ad_title_list if i not in stopword_list]

			#若要重建tfide model 下三段註解掉
			# load dictionary
			# dictionary = corpora.Dictionary.load('/Users/jack/Desktop/LDA/allnews_dictionary.dict')		 
			# # 建立語料庫
			# corpus = [dictionary.doc2bow(text) for text in texts_list]
			# # load tfidf model
			# tfidfModel = models.tfidfmodel.TfidfModel.load("/Users/jack/Desktop/LDA/tfidf_model.tfidf")

			
			# 重建tfidf model
			# dictionary = corpora.Dictionary(texts_list)
			# corpus = [dictionary.doc2bow(text) for text in texts_list]
			# tfidfModel = models.TfidfModel(corpus)

			###
			# LSI model
			lsi_title_sims_result = []
			for index in range(len(ad_title_list)):
			    texts_list = []
			    jieba_list = [data_title]
			    jieba_list.append(ad_title_list[index])
			    for i in jieba_list:
			        tokens = jieba.cut(i,cut_all=False,HMM=True)
			        stopped_tokens = [i for i in tokens if not i in stop_word_list]
			        texts_list.append(stopped_tokens)
			    # 重建tfidf model
			    dictionary = corpora.Dictionary(texts_list)
			    corpus = [dictionary.doc2bow(text) for text in texts_list]
			    tfidfModel = models.TfidfModel(corpus)
			    # 轉為向量表示
			    tfidfVectors = tfidfModel[corpus]

			    # 建立lsi model
			    lsi_model = models.LsiModel(tfidfVectors, id2word=dictionary, num_topics=2)

			    # 建立索引
			    indexLSI = similarities.MatrixSimilarity(lsi_model[corpus])
			    # 相似度
			    sims = indexLSI[lsi_model[dictionary.doc2bow(texts for texts in data_title)]]
			    lsi_title_sims_result.append([index, ad_title_list[index], sims[1]])

			    #整理為[ad_index, ad_title, ad_context, ad_sims, ad_amount, lda_ad_result, hit_time]
			    ad_list = []
				for i in range(len(lsi_title_sims_result)):
					ad_id = ad_data[i][0]
					ad_title = ad_data[i][1]
					ad_context = ad_data[i][2]
					ad_sims = ad_sims_list[i][1]
					ad_amount = ad_data[i][3]
					lda1_ad = ad_data[i][4]
					lda2_ad = ad_data[i][5]
					ad_list.append([ad_id, ad_title, ad_context, ad_sims, ad_amount, lda1_ad, lda2_ad, hit_time])




				# 設定門檻值
				sims_threshold = 1
				qty_threshold  = 10
				# 內文門檻值
				context_sims_threshold = 0.8

				1st_select_ad_list = []
				select_ad_list = []
				not_select_ad_list = []

				for i in range(len(ad_list)):
					if ad_list[i][3] >= sims_threshold:
						1st_select_ad_list.append(ad_list[i])
					else:
						not_select_ad_list.append(ad_list[i])

				# 如果選擇的廣告太多,再進行文章內容相關性分析
				if len(1st_select_ad_list) >= qty_threshold:
					ad_context_list = []
					for i in range(len(1st_select_ad_list)):
						ad_title_list.append(str(1st_select_ad_list[i][1]))

					for index in range(len(ad_context_list)):
					    texts_list = []
					    jieba_list = [data_context]
					    jieba_list.append(ad_context_list[index])
					    for i in jieba_list:
					        tokens = jieba.cut(i,cut_all=False,HMM=True)
					        stopped_tokens = [i for i in tokens if not i in stop_word_list]
					        texts_list.append(stopped_tokens)
					    # 重建tfidf model
					    dictionary = corpora.Dictionary(texts_list)
					    corpus = [dictionary.doc2bow(text) for text in texts_list]
					    tfidfModel = models.TfidfModel(corpus)
					    # 轉為向量表示
					    tfidfVectors = tfidfModel[corpus]

					    # 建立lsi model
					    lsi_model = models.LsiModel(tfidfVectors, id2word=dictionary, num_topics=2)

					    # 建立索引
					    indexLSI = similarities.MatrixSimilarity(lsi_model[corpus])
					    # 相似度
					    sims = indexLSI[lsi_model[dictionary.doc2bow(texts for texts in data_title)]]
					    if sims[1] >= context_sims_threshold:
					    	select_ad_list.append([1st_select_ad_list[index], sims[1]])
					    else:
					    	not_select_ad_list.append([1st_select_ad_list[index], sims[1]])

				else:
					select_ad_list = 1st_select_ad_list


			#排序相關性由高至低
			select_ad_list = sorted(select_ad_list, key=lambda x:x[3], reverse=True)       

			

			# 轉為向量表示
			#tfidfVectors = tfidfModel[corpus]
			# load lda model
			#ldamodel = models.ldamodel.LdaModel.load('/Users/jack/Desktop/LDA/allnews_LDA_model.lda')
			#corpus_lda = ldamodel.get_document_topics(tfidfVectors ,minimum_probability=0)
			# 建立索引
			#indexLDA = similarities.MatrixSimilarity(ldamodel[tfidfVectors])
			#indexLDA = similarities.MatrixSimilarity(corpus_lda)

			# 以新聞內容作為比較基準

			# sims = indexLDA[ldamodel[dictionary.doc2bow(text for text in data_title)]]
			# 排列相似度由大至小
			# ad_sims_list = sorted(enumerate(ad_sims_list), key=lambda item: -item[1])
			#####

			#整理為[ad_id, ad_title, ad_context, ad_sims, ad_amount, lda_ad_result, hit_time]	

			# [token_id, user_model_train_over, user_model]
			# 轉為dict = {token : model} 形式
			# token_list = []
			# model_list = []
			# for i in range(len(user_list)):
			# 	token_list.append(user_list[i][0])
			# 	model_list.append(user_list[i][2])
		    
			# dict_token_model = dict(zip(token_list, model_list))


			#push_ad_list = ml_select_ad_with_news.select_ad_to_user(ad_user_list, ad_list)


			#user = [token_id, user_model]

			#依新聞相關性媒合
			for select_ad in select_ad_list:

			    if select_ad[4] == 0:
			        break
			    else:
			        if len(data_token) > select_ad[4]:
			            select_user_for_ad = random.sample(data_token,select_ad[4])
			            select_ad.append(select_user_for_ad)
			            data_token = list(set(data_token) - set(select_user_for_ad))
			            select_ad[4] = int(select_ad[4]) - len(select_user_for_ad)
			        else:
			            select_ad.append(data_token)
			            select_ad[4] = int(select_ad[4]) - len(data_token)
			            data_token = []

			#get all user取得模型
			db = connect_mysql('db_owl', 'ML_user_data')
			cursor = db.cursor()

			limit_by_day  			 = 20
			limit_by_hour 			 = 3
			limit_by_mom  			 = 99

			# get all user取得模型
			user_list = select_user.select_user(db,
				limit_by_day, 
				limit_by_hour, 
				limit_by_mom, 
				web_id,
				category_id,
				)

			cursor.close()

			#將模型加入list進行LR分類
			dict_token_model = {}
			for user in user_list:
				dict_token_model[user[0]] = user[2]

			ad_user_list = []
			for token in data_token:
				ad_user_list.append([token, dict_token_model[token]])


			#媒合剩餘廣告
			if ad_user_list != []:
				#增加在list內的index
			    not_select_ad_list_with_index = list(enumerate(not_select_ad_list))
			    for user in ad_user_list:
			        try:
			        	user_model = user[1]
			        except:
			        	user_model = '_'

			        if user_model != '_':

			            for re_select_ad in not_select_ad_list_with_index:
			                re_select_ad_result = []
			                #判斷廣告是否還有額度
			                if re_select_ad[1][4] == 0:
			                    break
			                else:
			                    #轉換為浮點數再放入model        
			                    user_model = [float(coef_i) for coef_i in user[1].split(',')]
			                    lda_select_ad = [float(ad_i) for ad_i in re_select_ad[1][5].split(',')]
			                    [category_hour, category_week] = LR_function.categorize_time(re_select_ad[1][7])
			                    hit_time = [category_hour[:-1] + category_week[:-1]]
			                    prob = LR_function.prediction(user_model, lda_select_ad, hit_time)
			                    re_select_ad_result.append([re_select_ad[0], prob])
		                    #排序廣告與User之相關性
		                    re_select_ad_result = sorted(re_select_ad_result, key=lambda x:x[1], reverse=True)
		                    #最佳ad的index
		                    best_select_ad = re_select_ad_result[0]
		                    #檢查是否已經有user
		                    if len(not_select_ad_list_with_index[best_select_ad][1]) > 8:
		                        not_select_ad_list_with_index[best_select_ad][1][8].append(user)
		                    else:
		                        not_select_ad_list_with_index[best_select_ad][1].append([user])

		                    not_select_ad_list_with_index[best_select_ad][1][4] = int(not_select_ad_list_with_index[best_select_ad][1][4]) - 1
		                    ad_user_list.remove(user)            

			        #若沒有模型則隨機挑選廣告給User
			        else:
			            random_select_ad = random.choice(not_select_ad_list_with_index)
			            #判斷廣告是否還有額度
			            if random_select_ad[1][4] == 0:
			                #重新隨機選擇廣告
			                random_select_ad = random.choice(not_select_ad_list_with_index)
			            else:
			            	#檢查是否已經有user
			                if len(not_select_ad_list_with_index[random_select_ad[0]][1]) > 8:
			                    not_select_ad_list_with_index[random_select_ad[0]][1][8].append(user)
			                else:
			                    not_select_ad_list_with_index[random_select_ad[0]][1].append([user])


			                random_select_ad[1][4] = int(random_select_ad[1][4]) - 1
			                ad_user_list.remove(user)
			else:
			    pass

			#整理為原來格式
			need_select_ad_list = []
			for i in range(len(not_select_ad_list_with_index)):
    			need_select_ad_list.append(not_select_ad_list_with_index[i][1])

			#將兩次媒合的結果結合
			push_ad_list = []
			all_ad_list = select_ad_list + need_select_ad_list
			for ad in all_ad_list:
				if len(ad) > 8:
					push_ad_list.append(ad)

			#
			# if push_ad_list != []:
			# 	for push_ad_index in range(len(push_ad_list)):
			# 		push_channel = web_id_setting[1]

			# 		# likr
			# 		if push_channel == 1:
						
			# 			if push_times == None or push_times == 0:
			# 				cust_push_id = all_data['cust_push_id']
			# 			else:
			# 				cust_push_id = str(all_data['cust_push_id']) + '_' + str(push_times)
			# 			web_id 			 = all_data['web_id']
			# 			category_id 	 = all_data['category_id']
			# 			audience 		 = all_data['amount']
			# 			title 			 = all_data['title']
			# 			msg 			 = all_data['paragraph']
			# 			icon 			 = all_data['icon']
			# 			leading 		 = all_data['url']
			# 			bigimage 		 = all_data['img_id']



			# 			button_one_title = push_ad_list[push_ad_index][1]
			# 			button_one_icon  = all_data['btn_1_icon']
			# 			button_one_url   = all_data['btn_1_url']
			# 			button_two_title = all_data['btn_2_title']
			# 			button_two_icon  = all_data['btn_2_icon']
			# 			button_two_url   = all_data['btn_2_url']
			# 			tag 			 = all_data['renotify_tag']

			# 			token_group_index = 5000

			# 			token_list = push_ad_list[push_ad_index][6]
			# 			len_token = len(token_list)

			# 			for i in range(0, len_token, token_group_index):
			# 				token = ','.join(token_list[i:i+token_group_index])

			# 				payload = {
			# 					'type'			   : '1',
			# 					'cust_push_id'	   : cust_push_id,
			# 					'web_id'           : web_id,
			# 					'category_id'      : category_id,
			# 					'token'            : token
			# 					}

			# 				url       = crm_push_api
			# 				headers   = {'content-type': 'application/x-www-form-urlencoded'}
			# 				push_data = json.dumps(payload)
			# 				response  = requests.post(url,data=push_data,headers=headers)


			# 			# job of type 1 (send token) over and then send type 2 payload to start push
			# 			payload = {
			# 				'type'				: '2',
			# 				'cust_push_id'		: cust_push_id,
			# 				'web_id'			: web_id,
			# 				'category_id'		: category_id,
			# 				'audience'			: audience,
			# 				'title'				: title,
			# 				'msg'				: msg,
			# 				'icon'				: icon,
			# 				'leading'			: leading,
			# 				'bigimage'			: bigimage,
			# 				'button_one_title'	: button_one_title,
			# 				'button_one_icon'	: button_one_icon,
			# 				'button_one_url'	: button_one_url,
			# 				'button_two_title'	: button_two_title,
			# 				'button_two_icon'	: button_two_icon,
			# 				'button_two_url'	: button_two_url,
			# 				'renotify'			: 'true',
			# 				'tag'				: tag
			# 				}

			# 			url       = crm_push_api
			# 			headers   = {'content-type': 'application/x-www-form-urlencoded'}
			# 			push_data = json.dumps(payload)
			# 			response  = requests.post(url,data=push_data,headers=headers)

			# 			if push_times == None or push_times == 0:
			# 				write_log(str(all_data['cust_push_id']) + ':' + response.text)
			# 				# 儲存push id(msg id)
			# 				save_push_id_data(all_data['web_id'], all_data['cust_push_id'], '_')
			# 			else:
			# 				write_log(str(all_data['cust_push_id']) + '_' + str(push_times) + ':' + response.text)
			# 				# 儲存push id(msg id)
			# 				save_push_id_data(all_data['web_id'], all_data['cust_push_id'] + '_' + str(push_times), '_')

						
			# 		# onesignal
			# 		elif push_channel == 2 :

			# 				app_id 	 = web_id_setting[2]
			# 				rest_key = web_id_setting[3]

			# 				send_data = {
			# 					'app_id': app_id,	
			# 					'headings': {
			# 						'zh-Hant' : all_data['title'],
			# 						'en'      : all_data['title']
			# 					},
			# 					'contents' : {
			# 						'zh-Hant' : all_data['paragraph'],
			# 						'en'      : all_data['paragraph']
			# 					},
			# 					'include_player_ids' : push_ad_list[push_ad_index][6],
			# 					'url'                : all_data['url']
			# 				}

			# 				if all_data['icon'] != '_':
			# 					send_data['chrome_web_icon'] = all_data['icon']

			# 				if all_data['img_id'] != '_':
			# 					send_data['chrome_web_image'] = all_data['img_id']

			# 				if all_data['btn_1_title'] != '_' or all_data['btn_1_icon'] != '_' or all_data['btn_1_url'] != '_' or all_data['btn_2_title'] != '_' or all_data['btn_2_icon']  != '_' or all_data['btn_2_url'] != '_' :
			# 					send_data['web_buttons'] = []

			# 					if all_data['btn_1_title'] != '_' or all_data['btn_1_icon'] != '_' or all_data['btn_1_url'] != '_' :
			# 						send_data['web_buttons'].append({'id' : 'button1'})

			# 						if all_data['btn_1_title'] != '_' : 
			# 							send_data['web_buttons'][0]['text'] = push_ad_list[push_ad_index][1]

			# 						if all_data['btn_1_url'] != '_' : 
			# 							send_data['web_buttons'][0]['url'] = all_data['btn_1_url']

			# 						if all_data['btn_1_icon'] != '_' : 
			# 							send_data['web_buttons'][0]['icon'] = all_data['btn_1_icon']

			# 					if all_data['btn_2_title'] != '_' or all_data['btn_2_icon'] != '_' or all_data['btn_2_url'] != '_' :
			# 						send_data['web_buttons'].append({'id' : 'button2'})

			# 						if all_data['btn_2_title'] != '_' :
			# 							try: 
			# 								send_data['web_buttons'][1]['text'] = all_data['btn_2_title']
			# 							except:
			# 								send_data['web_buttons'][0]['text'] = all_data['btn_2_title']

			# 						if all_data['btn_2_url'] != '_' : 
			# 							try:
			# 								send_data['web_buttons'][1]['url'] = all_data['btn_2_url']
			# 							except:
			# 								send_data['web_buttons'][0]['url'] = all_data['btn_2_url']

			# 						if all_data['btn_2_icon'] != '_' : 
			# 							try:
			# 								send_data['web_buttons'][1]['icon'] = all_data['btn_2_icon']
			# 							except:
			# 								send_data['web_buttons'][0]['icon'] = all_data['btn_2_icon']


			# 					send_data = json.dumps(send_data)
			# 					os_push_api ='https://onesignal.com/api/v1/notifications'

			# 					headers = {'Authorization': 'Basic ' + str(rest_key),
			# 								'Content-Type': 'application/json; charset=utf-8'}

			# 					response = requests.post(os_push_api, data = send_data, headers = headers)
			# 					onesignal_resp = json.loads(response.text)
			# 					print(send_data)
			# 					print(onesignal_resp)
						
			# 					# 儲存push id(msg id)
			# 					save_push_id_data(all_data['web_id'], all_data['cust_push_id'], onesignal_resp['id'])

			# 					# 若有失效token 則更新
			# 					if 'errors' in onesignal_resp:
			# 						for invalid_token in onesignal_resp['errors']:
			# 							update_invalid_token(all_data['web_id'], invalid_token)

			# 					if push_times == None or push_times == 0:
			# 						write_log(str(all_data['cust_push_id']) + ':' + response.text)
			# 						# 儲存push id(msg id)
			# 						save_push_id_data(all_data['web_id'], all_data['cust_push_id'], onesignal_resp['id'])
			# 					else:
			# 						write_log(str(all_data['cust_push_id']) + '_' + str(push_times) + ':' + response.text)
			# 						# 儲存push id(msg id)
			# 						save_push_id_data(all_data['web_id'], all_data['cust_push_id'] + '_' + str(push_times), onesignal_resp['id'])


			
			# else:
			# 	pass


			# #如果
			# if ad_user_list != []:
			# 	push_channel = web_id_setting[1]
			# 	if push_channel == 1:
			# 		if news_page_special.whether_attach_landing_page(web_id) and web_id in ['some web id']:

			# 			payload      = {'url':data_url,
			# 							'title':new_data_title,
			# 							'token':ad_user_list,
			# 							'paragraph':new_data_context,
			# 							'amount':str(len(this_push_tokens)),
			# 							'img_id':data_img,
			# 							'web_id':web_id,
			# 							'category_id':category_id,
			# 							'cust_push_id':str(max_url_id),
			# 							'renotify_tag':str((max_url_id  % renotify_tag_number) + 1),
			# 							'icon':msg['icon'],
			# 							'btn_1_title':'猜你喜歡的新聞',
			# 							'btn_1_icon':'_',
			# 							'btn_1_url':landing_page_list[web_id],
			# 							'btn_2_title':'_',
			# 							'btn_2_icon':'_',
			# 							'btn_2_url':'_'
			# 							}
			# 		else:

			# 			payload      = {'url':data_url,
			# 							'title':new_data_title,
			# 							'token':ad_user_list,
			# 							'paragraph':new_data_context,
			# 							'amount':str(len(this_push_tokens)),
			# 							'img_id':data_img,
			# 							'web_id':web_id,
			# 							'category_id':category_id,
			# 							'cust_push_id':str(max_url_id),
			# 							'renotify_tag':str((max_url_id  % renotify_tag_number) + 1),
			# 							'icon':msg['icon'],
			# 							'btn_1_title':'關注',
			# 							'btn_1_icon':'_',
			# 							'btn_1_url':'close',
			# 							'btn_2_title':'不喜歡',
			# 							'btn_2_icon':'_',
			# 							'btn_2_url':'close'
			# 							}

			# 	elif push_channel == 2:

			# 		app_id 	 = web_id_setting[2]
			# 		rest_key = web_id_setting[3]

			# 		send_data = {
			# 			'app_id': app_id,	
			# 			'headings': {
			# 				'zh-Hant' : all_data['title'],
			# 				'en'      : all_data['title']
			# 			},
			# 			'contents' : {
			# 				'zh-Hant' : all_data['paragraph'],
			# 				'en'      : all_data['paragraph']
			# 			},
			# 			'include_player_ids' : ad_user_list,
			# 			'url'                : all_data['url']
			# 		}

			# 		if all_data['icon'] != '_':
			# 			send_data['chrome_web_icon'] = all_data['icon']

			# 		if all_data['img_id'] != '_':
			# 			send_data['chrome_web_image'] = all_data['img_id']



		
			print(push_ad_list)


			os.remove(file)


	else:
		time.sleep(5)












