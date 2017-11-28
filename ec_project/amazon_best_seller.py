#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zengls on 2017/11/28

import requests
from lxml import etree
import pandas as pd
from fake_useragent import UserAgent
import time

ua = UserAgent(verify_ssl=False)
headers= {}
# headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'

#获取单页链接的产品信息
def get_product(url,products):
    headers['User-Agent'] = ua.random
    response = requests.get(url, headers=headers)
    response.coding = 'utf-8'
    # x_path = '//div[@class="zg_itemWrapper"]/div/a/div[@class="p13n-sc-truncated-hyphen p13n-sc-truncated"]'
    content = etree.HTML(response.text)
    titles = content.xpath('//div[@class="zg_itemWrapper"]/div/a/div/text()')
    comments = content.xpath('//*[@id="zg_centerListWrapper"]/div/div[2]/div/div[1]')
    prices = content.xpath('//div[@class="zg_itemWrapper"]')
    ids = content.xpath('//*[@id="zg_centerListWrapper"]/div/div[1]/span/text()')
    links = content.xpath('//div[@class="zg_itemWrapper"]/div/a/@href')
    for title in titles:
        products['title'].append(title.strip())
    for comment in comments:
        comment = comment.xpath('./a[2]/text()')
        if len(comment) == 0:
            products['comment'].append('None')
        else:
            products['comment'].append(comment[0])
    for price in prices:
        price = price.xpath('./div/div/span/span/text()')
        if len(price) == 0:
            products['price'].append('None')
        else:
            products['price'].append(price[0].strip())
    for id in ids:
        products['rank'].append(id.strip())
    for link in links:
        link = 'https://www.amazon.com' + link
        products['link'].append(link)
#储存数据
def save_data(products,filename):
    df = pd.DataFrame(products)
    df.index = df['rank']
    del df['rank']
    df.to_excel(filename + '.xls')

#获取该热销下的所有产品，每个热销均100个产品
def get_pages(main_url):
    products = {'comment': [], 'price': [], 'title': [], 'rank': [],'link':[]}
    name = main_url.split('/')[3]
    for i in range(5):
        url = main_url + '?_encoding=UTF8&pg=%s'%str(i+1)
        get_product(url,products)
        time.sleep(1)
        print('成功抓取第%s页'%str(i+1))
    save_data(products,name)

#抓取以下链接
url_list = ["https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_unv_e_1_689637011_3",
"https://www.amazon.com/gp/bestsellers/electronics/502394/ref=cam_acc_nav_bestsellersp/ref=s9_acss_bw_ln_camcolla_3_9_w?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-leftnav&pf_rd_r=4QBB036XW839PAJ3EYQD&pf_rd_r=4QBB036XW839PAJ3EYQD&pf_rd_t=101&pf_rd_p=879df478-aae2-41c3-b289-a27e8dbefd23&pf_rd_p=879df478-aae2-41c3-b289-a27e8dbefd23&pf_rd_i=502394",
"https://www.amazon.com/best-sellers-video-games/zgbs/videogames/ref=sv_vg_12",
"https://www.amazon.com/Best-Sellers-Electronics-Audio-Headphones/zgbs/electronics/172541/ref=zg_bs_nav_e_1_e",
"https://www.amazon.com/Best-Sellers-Electronics-Home-Audio-Theater-Products/zgbs/electronics/667846011/ref=zg_bs_nav_e_1_e",
"https://www.amazon.com/Best-Sellers-Electronics-Portable-Audio-Video/zgbs/electronics/172623/ref=zg_bs_nav_e_1_e",
"https://www.amazon.com/Best-Sellers-Electronics-Security-Surveillance-Equipment/zgbs/electronics/524136/ref=zg_bs_nav_e_1_e",
"https://www.amazon.com/Best-Sellers-Electronics-Video-Game-Consoles-Accessories/zgbs/electronics/7926841011/ref=zg_bs_nav_e_1_e",
"https://www.amazon.com/Best-Sellers-Electronics-Wearable-Technology/zgbs/electronics/10048700011/ref=zg_bs_nav_e_1_e",
"https://www.amazon.com/Best-Sellers-Womens-Handbags-Purses/zgbs/fashion/15743631/ref=zg_bs_nav_2_7147440011"]
count = 0
start_time = time.time()
for main_url in url_list:
    try:
        get_pages(main_url)
        print('第%s个链接抓取并存储完毕'%str(count+1))
        count += 1
    except:
        print('重新连接。')
        get_pages(main_url)
stop_time = time.time()
print('%s个链接抓取完毕，总共使用%s秒'%(str(count),str(stop_time-start_time)))



