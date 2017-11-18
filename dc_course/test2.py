#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zengls on 2017/11/16
import random
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import re
from pymongo import MongoClient

browser = webdriver.Chrome()
browser.set_window_size(1120, 550)#使用phantomJS添加窗口可加载js
wait = WebDriverWait(browser,10)
browser.get('https://www.taobao.com')
inputbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
clickbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
inputbox.clear()
inputbox.send_keys(u'键盘')
clickbox.click()
def is_element_exist(locator):
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,locator)))
    except:
        return False
    return True
if is_element_exist('.total.link'):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.total.link'))).click()
total_pages = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager>div>div>div>div.total'))).text
print(total_pages)



# ua = UserAgent()
#
# for i in range(1,10):
#     # print(random.random()*3)
#     # print(ua.random)
#     print(i)
# if __name__ == '__main__':
#     pass