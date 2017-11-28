#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zengls on 2017/11/18
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import re
from pymongo import MongoClient

class TaobaoSpider(object):
    def __init__(self,keyword,page_num):
        self.keyword = keyword
        self.page_num = page_num
        self.check_page_num()
        #初始化浏览器并连接数据库
        self.browser = webdriver.Chrome()  # 使用phantomJS无头浏览器会被识别爬虫
        self.browser.set_window_size(1120, 550)  # 使用phantomJS添加窗口可加载js
        self.wait = WebDriverWait(self.browser, 10)
        self.connection = MongoClient()
        self.db = self.connection.taobao
        self.collection_name = 'taobao_by_keyword'
        self.collection = self.db[self.collection_name]

    def check_page_num(self):
        if type(self.page_num) != int:
            print('Please input an int number.')
            raise SystemExit
        if self.page_num > 100:
            print('%s is an illegal page number.'%str(self.page_num))
            raise SystemExit


    # 进入淘宝网，输入关键字，返回页面,并通过递归重连
    def search_keyword(self):
        try:
            self.browser.get('https://www.taobao.com')
            inputbox = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
            clickbox = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
            # located by id and clss
            # inputbox = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="q"]')))
            # clickbox = wait.until(EC.presence_of_element_located((By.XPATH,'//button[@class="btn-search tb-bg"]')))
            inputbox.clear()
            inputbox.send_keys(self.keyword)
            clickbox.click()
            # 判断是否为店铺汇总页
            if self.is_element_exist('.total.link'):
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.total.link'))).click()
            total_pages = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager>div>div>div>div.total'))).text
            # total_pages = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'total'))).text
            print('获得页面')

            # get_products()
            # print('获得详情')
            # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
            # total_pages = re.search('\d+',total_pages).group(0) ##正则提取页数
            return total_pages
        except TimeoutException:
            print('无法连接，重新获取。')
            self.search_keyword()

    # 翻页功能
    def next_page(self,present_page_num):
        try:
            inputbox = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager>div>div>div>div.form>input')))
            buttonbox = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#mainsrp-pager>div>div>div>div.form>span.btn.J_Submit')))
            inputbox.clear()
            inputbox.send_keys(present_page_num)
            buttonbox.click()
            self.wait.until(EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#mainsrp-pager>div>div>div>ul>li.item.active>span'), str(present_page_num)))
            self.get_products()
        except:
            self.next_page(present_page_num)

    # 获得产品信息
    def get_products(self):
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))  # 父子元素class属性之间需要空格
        html = self.browser.page_source
        doc = pq(html)
        items = doc('#mainsrp-itemlist .items .item').items()

        for item in items:
            products = {
                'catalogue': self.keyword,
                'title': item.find('.title').text(),
                'price': item.find('.price').text(),
                'deal': item.find('.deal-cnt').text(),
                'image': item.find('.pic .img').attr('src'),
                'shop': item.find('.shop').text(),
                'location': item.find('.location').text(),
            }
            self.collection.insert(products)

    # 判断元素是否存在
    def is_element_exist(self,locator):
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))
        except:
            return False
        return True

    def get_by_keyword(self):
        total = self.search_keyword()
        total = re.search('\d+', total).group()
        print('关键词为\'%s\'的商品共%s页.' % (self.keyword, str(total)))
        for i in range(1, self.page_num + 1):
            print('爬取第%s页...' % str(i))
            self.next_page(i)
            print('第%s页存储成功' % str(i))
        print('爬取完毕！')
        #关闭浏览器
        self.browser.close()

##***********************以上为按类设计********************************
'''
browser = webdriver.Chrome()#使用phantomJS无头浏览器会被识别爬虫
browser.set_window_size(1120, 550)#使用phantomJS添加窗口可加载js
wait = WebDriverWait(browser,10)
connection = MongoClient()
db = connection.taobao
collection = db.products


#进入淘宝网，输入关键字，返回页面
def search_keyword(keyword='裤子'):
    try:
        browser.get('https://www.taobao.com')
        inputbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
        clickbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        #located by id and clss
        # inputbox = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="q"]')))
        # clickbox = wait.until(EC.presence_of_element_located((By.XPATH,'//button[@class="btn-search tb-bg"]')))
        inputbox.clear()
        inputbox.send_keys(keyword)
        clickbox.click()
        #判断是否为店铺汇总页
        if is_element_exist('.total.link'):
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.total.link'))).click()
        total_pages = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager>div>div>div>div.total'))).text
        # total_pages = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'total'))).text
        print('获得页面')

        # get_products()
        # print('获得详情')
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
        # total_pages = re.search('\d+',total_pages).group(0) ##正则提取页数
        return total_pages
    except TimeoutException:
        search_keyword()

#翻页功能
def next_page(page_num,keyword):
    try:
        # print('翻页测试点1.')
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
        inputbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager>div>div>div>div.form>input')))
        # print('翻页测试点2.')
        buttonbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager>div>div>div>div.form>span.btn.J_Submit')))
        # print('翻页测试点3.')
        inputbox.clear()
        inputbox.send_keys(page_num)
        buttonbox.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager>div>div>div>ul>li.item.active>span'),str(page_num)))
        get_products(keyword)
    except:
        next_page(page_num)

#test area
# browser.get('https://www.taobao.com')
# site_region = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'site-nav-region'))).text
# print(site_region)

#获得产品信息
def get_products(keyword):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))  #父子元素class属性之间需要空格
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()

    for item in items:
        products = {

            'catalogue':keyword,
            'title':item.find('.title').text(),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text(),
            'image':item.find('.pic .img').attr('src'),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text(),
        }
        collection.insert(products)

#判断因素是否存在
def is_element_exist(locator):
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,locator)))
    except:
        return False
    return True
def main(keyword,num):
    total = search_keyword(keyword)
    total = re.search('\d+', total).group()
    print('关键词为\'%s\'的商品共%s页.'%(keyword,str(total)))
    for i in range(1,num+1):
        print('爬取第%s页...'%str(i))
        next_page(i,keyword)
        print('第%s页存储成功' % str(i))
    print('爬取完毕！')
'''
if __name__ == '__main__':
    # print('hello taobao,I am coming.')
    # main('剃须刀',50)
    # total = search_keyword()
    # total = re.search('\d+', total).group()
    # for i in range(1,4):
    #     print('爬取第%s页...'%str(i))
    #     next_page(i)
    #     print('第%s页存储成功' % str(i))
    # print('爬取完毕！')
    tb = TaobaoSpider('新秀丽',100)
    tb.get_by_keyword()