#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zengls on 2017/11/24

# from selenium import webdriver
#
# # browser = webdriver.Chrome('C:/Users/adam/AppData/Local/Google/Chrome/Application/chromedriver.exe')
# browser = webdriver.Chrome()
# browser.get('http://www.baidu.com')

def test(num):
    try:
        type(num) == int
        print('数字')
    except:
        print('非数字')
import requests
from fake_useragent import UserAgent
# ua = UserAgent(verify_ssl=False)

assert isinstance(2,int),'err'