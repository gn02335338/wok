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
from lda_sims import news_ad_sims
from LR_function import categorize_time, prediction


def get_ad_data(db, ad_id):
	cursor = db.cursor()

	# sql query
	sql = "SELECT AD_context, AD_amount,  FROM AD_index WHERE id = %s " % ad_id

	ursor.execute(sql)
	ad_data = cursor.fetchall()
	cursor.close()

	ad_data = sql_result

	return ad_data


def select_ad_to_user(user_list, ad_list):
	
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

	##user = [token_id, user_model_train_over, user_model]
	#user = [token_id, user_model]	


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

	

	#媒合剩餘廣告
	while user_list != [] and not_select_ad_list != []:
        for user in user_list:
#			user_model_train_over = int(user[1])
#			if user_model_train_over == 1:
			user_model = user[1]
			if user_model != '_':

                for re_select_ad in not_select_ad_list:
                    re_select_ad_result = []
                    #判斷廣告是否還有額度
                    if re_select_ad[3] == 0:
                        not_select_ad_list.remove(re_select_ad)
                    else:
                    	#轉換為浮點數再放入model        
                        user_model = [float(coef_i) for coef_i in user[1].split(',')]
                        lda_select_ad = [float(ad_i) for ad_i in re_select_ad[4].split(',')]
                        [category_hour, category_week] = LR_function.categorize_time(re_select_ad[5])
                        hit_time = [category_hour[:-1] + category_week[:-1]]
#						yhat = logistic_model.predicted_hit(lda_select_ad, hit_time, user_model)
						prob = LR_function.prediction(user_model, lda_select_ad, hit_time)
                        re_select_ad_result.append([re_select[0], prob, re_select[2]])
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
	
	return need_ad_token_index


if __name__ == '__main__':








