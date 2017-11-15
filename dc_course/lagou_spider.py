#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zengls on 2017/11/15
import requests
from fake_useragent import UserAgent
from pymongo import MongoClient
import time
from lxml import etree

url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
ua = UserAgent()
random_ua = ua.random
headers_detail = {'User-Agent': random_ua}
#创建数据库
connection = MongoClient()
db = connection.lagou_db
collection = db.jobs

#抓取多页职位
def get_pages_data(page,position):
    for i in range(page):
        random_ua = ua.random
        headers = {
            'User-Agent': random_ua,
            'Cookie': 'user_trace_token=20171019091536-0358c02b-b46b-11e7-9c41-525400f775ce; LGUID=20171019091536-0358c3d8-b46b-11e7-9c41-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAACBHABBI2F95E736604692F120C8CA58700D7F5E; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_search; SEARCH_ID=55ed20fb2bd94f5388efbd71d298eb54; _gid=GA1.2.922181100.1510733125; _ga=GA1.2.2063843603.1508375738; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1509939997,1509940512,1510305660,1510733125; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1510733140; LGSID=20171115160525-bc5556ee-c9db-11e7-98e9-5254005c3644; LGRID=20171115160540-c53549b9-c9db-11e7-9088-525400f775ce',
            'Referer': 'https://www.lagou.com/jobs/list_%E5%95%86%E5%8A%A1%E7%BB%8F%E7%90%86?labelWords=&fromSearch=true&suginput='
        }
        payload = {
            'first':'false',
            'pn':str(i+1),
            'kd':position
        }
        response = requests.post(url,data=payload,headers=headers).json()['content']['positionResult']['result']
        print('第%s页数据抓取完毕！'%str(i+1))
        time.sleep(1.5)
        print(response)
        # print(random_ua)
        collection.insert(response)  #存储数据
        print('第%s页数据存储完毕！' % str(i + 1))


if __name__ == '__main__':
    # get_pages_data(20,'数据挖掘')
    # get_position_detail(url,db)
    pass
