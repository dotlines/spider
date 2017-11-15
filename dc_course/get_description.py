#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zengls on 2017/11/15
import requests
from lxml import etree
from pymongo import MongoClient
from fake_useragent import UserAgent
import time
import random

ua = UserAgent()




connection = MongoClient()
db = connection.lagou_db
collection = db.jobs
back = collection.find({}, {'positionId':1,'positionName':'1','_id':0})
# proxies = { "http": "http://10.10.1.10:3128", "https": "http://10.10.1.10:1080", }
def get_position_detail(position_url):
    random_ua = ua.random
    # random_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    # 添加cookies反爬

    headers_detail = {
        'User-Agent': random_ua,
        'Cookie': 'user_trace_token=20170427221530-8703b88db6a14dc8a87efc87acc4d36e; LGUID=20170427221530-f87ad33c-2b53-11e7-b407-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=83d99db100dc17222f07b863680088db; _gat=1; _ga=GA1.2.1838507030.1493302530; _gid=GA1.2.514539880.1510754929; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1510067115,1510754929; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1510765515; LGSID=20171115235515-5efa1137-ca1d-11e7-98f7-5254005c3644; LGRID=20171116010512-2497223f-ca27-11e7-918f-525400f775ce',
        'Host': 'm.lagou.com',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Connection':'keep-alive',
        # 'Accept-Encoding':'gzip, deflate, br',
        # 'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        # 'Upgrade-Insecure-Requests':'1',
        # 'Cache-Control':'max-age=0'
    }
    try:
        detail_response = requests.get(position_url, headers=headers_detail)
        detail_response.encoding = 'utf-8'
        r = etree.HTML(detail_response.text)
        # description = r.xpath('string(//dd[@class="job_bt"]/div)')
        description = r.xpath('//title/text()')  #测试反爬
        return description
    except:
        return '抓取异常'

count = 0
collection = db.description
# descriptions = []
for item in back:
    position_url = 'https://m.lagou.com/jobs/%s.html' % item['positionId']
    job_description = get_position_detail(position_url)
    rand = random.random()*5
    time.sleep(rand)
    # print('第%s个岗位抓取成功！'%str(count+1))
    # collection.insert({'链接':position_url,'岗位描述':job_description,'职位':item['positionName']})
    # print('第%s个岗位入库成功！' % str(count + 1))
    # descriptions.append(job_description)
    print(job_description,rand)
    # print('------------------第%s页--------------------'%(count+1))
    # print(position_url)
    count += 1
    # if count == 30:
    #     break



if __name__ == '__main__':
    # des = get_position_detail('https://www.lagou.com/jobs/3594019.html')
    # print(des)
    # collection.insert({'岗位描述':des})
    pass