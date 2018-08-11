import requests
import json
from lxml import etree
import io

citys = {}

url = 'https://www.lagou.com/gongsi/allCity.html?option=215-0-0'
response = requests.get(url)
html = etree.HTML(response.text)
# parser = etree.HTMLParser()
# html = etree.parse(io.StringIO('city.html'),parser=parser)
city_lists = html.xpath('//table[@class="word_list"]/tr/td/ul/li/a')
for city in city_lists:
	citys[city.xpath('string(.)')] = city.xpath('string(./@href)')

jsObj = json.dumps(citys,ensure_ascii=False)


with open('city.json','w') as cf:
	cf.write(jsObj)