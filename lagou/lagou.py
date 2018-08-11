import requests
from lxml import etree
import io
import json
from fake_useragent import UserAgent
import pymongo
from time import sleep

class Lagou(object):
	"""docstring for Lagou"""
	def __init__(self, city_name,page_number=1):
		self.city_name = city_name
		self.page_number = page_number
		

# url = 'https://www.lagou.com/gongsi/215-0-0.json'
	
# def city_url(city_name):
# 	with open('city.json','r') as cf:
# 		citys = json.load(cf)
# 	return citys[city_name]
ua = UserAgent()

myclient = pymongo.MongoClient('mongodb://localhost:27017')
mydb = myclient['lagoudb']
companies_col = mydb['company_smr'] 



def get_city_companys(city_name,**page_number):
	if page_number == None:
		pn = 100
	else:
		pn = page_number['page_number']
	with open('city.json','r') as cf:
		citys = json.load(cf)
	url = citys[city_name]
	headers = {
	'User-Agent':ua.random,
	'Referer':url,  #url without '.json'
	'Cookie':'JSESSIONID=ABAAABAAAFCAAEGBBB4142F20938248BB2478F3E58144AC; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533828435; _ga=GA1.2.270700076.1533828435; user_trace_token=20180809232715-b1c8888a-9be8-11e8-b9f2-525400f775ce; LGUID=20180809232715-b1c88c33-9be8-11e8-b9f2-525400f775ce; X_HTTP_TOKEN=3086fbe35a0d1fd40e7578a16f535b8b; _putrc=6F2F4FED79124B7A; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B73070; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%B9%BF%E5%B7%9E; TG-TRACK-CODE=index_search; _gid=GA1.2.105723379.1533990288; _gat=1; LGSID=20180811202447-89784d70-9d61-11e8-ba8e-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F2-0-0; gate_login_token=a11927046bd1035997e3d742392a2df46399e358fdcdf349; LGRID=20180811202449-8a37bc8c-9d61-11e8-ba8e-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533990289',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	# 'Cache-Control': 'max-age=0',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
	'Connection': 'keep-alive',
	'Content-Length': '39',
	'Host': 'www.lagou.com',
	# 'Upgrade-Insecure-Requests': '1',
	'Origin': 'https://www.lagou.com',
	# 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	# 'X-Anit-Forge-Code': '0',
	# 'X-Anit-Forge-Token': None,
	# 'X-Requested-With': 'XMLHttpRequest'
	}
	companies = []
	new_url = url + '.json'
	for i in range(pn):
		pyload={
			'pn':i + 1,#第0页和第1页是一样的
			'first': False,
			'havemark': 0,
			'sortField': 0
		}
		response = requests.post(new_url,headers=headers,data=pyload)
		company = json.loads(response.text)
		if not company['result']:
			break
		#数据存储至mongodb
		companies_col.insert(company)
		# print(type(company))
		print('NO. %d finished.'%(i+1))
		sleep(0.5)

	# print(companies)
	# print(new_url)
	#文本形式保存公司数据
	# with open('companies.txt','w') as f:
	# 	for company in companies:
	# 		f.write(company)
	# 		f.write('\n')

if __name__ == '__main__':
	get_city_companys('厦门',page_number=100)