#-*- conding:UFT-8 -*-

import urllib
import requests
import sys
import time
from bs4 import BeautifulSoup
from openpyxl import Workbook

hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

def book_spider(book_tag):
	pass

def get_people_num(url):
	pass

def do_spider(book_tag_lists):
	pass

def print_book_lists_excel(book_lists,book_tag_lists):
	pass


if __name__ == '__main__':
	book_tag_lists = []
	book_lists = do_spider(book_tag_lists)
	print_book_lists_excel(book_lists,book_tag_lists)