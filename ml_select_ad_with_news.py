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



def ad_







