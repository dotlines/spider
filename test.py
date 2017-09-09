import urllib.request
from bs4 import BeautifulSoup
import json



# url = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=20"
url = "http://geek.csdn.net/service/news/get_category_news_list?category_id=cloud&jsonpcallback=jQuery203015757937218031848_1504954168760&username=&from=60&size=20&type=category&_=1504954168763"
request = urllib.request.urlopen(url)
plain_text = str(request.read(),encoding='utf-8')
soup = BeautifulSoup(plain_text,'lxml')
lists = str(soup.find('p').string)
# lists = soup.findAll('dl',{'class':'geek_list'})

# for l in lists:
# 	title = l.find('a',{'class':'title'}).string
# 	print(title)
txt = open('test.txt','rb').read()
# json_str = json.loads(lists)
json_str = json.loads(txt)
# json_str = json.dumps(json_str,indent=4,ensure_ascii=False)
soup = BeautifulSoup(json_str['html'],'lxml')
lists = soup.findAll('dl',{'class':'geek_list'})
for l in lists:
	title = l.find('a',{'class':'title'}).string
	print(title)
# lists = soup.findAll('dl',{'class':'geek_list'})
# print(lists)
# print(json_str)