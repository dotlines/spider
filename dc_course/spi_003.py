# -*-coding:utf-8 -*-
import requests
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd


#通用爬虫框架
def getHTMLText(url):
	headers = {'user-agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'}
	try:
		r = requests.get(url,timeout=20,headers=headers)
		r.encoding = 'utf-8'
		# print(r.apparent_encoding)
		r.raise_for_status()
		#'utf-8'
		return r.text
	except:
		return '返回异常'
#结构化xml
def getxpath(html):
	return etree.HTML(html)

def getSoup(html):
	return BeautifulSoup(html,'lxml')

def getPageResult(url_pattern,page_num,xpath_pattern):
	comments = []
	for i in range(page_num):
		response = getHTMLText(url_pattern + str(i+1))
		s = etree.HTML(response)
		pattern = s.xpath(xpath_pattern)
		for item in pattern:
			print(item)
		comments.extend(pattern)
	return comments
def doSave(pattern):
	# save by open mathod
	# with open('comments.csv','w') as f:
	# 		f.write(which is always equal to
	# 		the length of the string)
			# print(item)

	#save by pandas
	df = pd.DataFrame(pattern)
	print(df)
	df.to_csv('comments.csv')

#爬去豆瓣图书的评论
# url_pattern = 'https://book.douban.com/subject/25862578/comments/hot?p='
# page_num = 5
# xpath_pattern = '//p[@class="comment-content"]/text()'
#
# comments = getPageResult(url_pattern, page_num, xpath_pattern)
# doSave(comments)
# print(comments)
# url = 'https://book.douban.com/subject/25862578/comments'
# response = getHTMLText(url)

# #xpath解析
# s = etree.HTML(response)
# pattern = s.xpath('//p[@class="comment-content"]/text()')
# comments = []
# print(s.xpath('//*[@id="comments"]/ul/li/div[2]/p/text()'))

# #beautiful soup解析
# soup = getSoup(response)
# pattern = soup.findAll('p','comment-content')
# comments = []
# for item in pattern:
# 	comments.append(item.text)
# print(comments)




#################################################

#爬去小猪短租的内容http://sz.xiaozhu.com/
# url = 'http://sz.xiaozhu.com/'
# response = getHTMLText(url)
# s = getxpath(response)
# print(s.xpath('//span[@class="result_title hiddenTxt"]/text()'))
# print(s.xpath('string(//span[@class="result_price"])'))
# for item in s.xpath('//span[@class="result_price"]'):
# 	print(item.xpath('string(.)'))
# print(s.xpath('//ul[@class="pic_list clearfix"]/li/@latlng'))
getHTMLText('https://www.lagou.com/jobs/496417.html')
