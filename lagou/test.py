import json
import pymongo
import csv




# print(data['result'][0])

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['lagoudb']
# city_col = mydb['city']
com_col = mydb.company_smr

print(com_col.find()[0]['result'][0].keys())

with open('xm_company.csv','w') as f:
	writer = csv.writer(f)
	field_list = list(com_col.find()[0]['result'][0].keys())
	writer.writerow(field_list)

	for companyList in com_col.find():
		# print(companyList['result'])
		for company in companyList['result']:
			rowdata = [company['companyId'],company['companyFullName'],company['companyShortName'],company['companyLogo'],company['city'],company['industryField'],company['companyFeatures'],company['financeStage'],company['companySize'],company['interviewRemarkNum'],company['positionNum'],company['processRate'],company['approve'],company['countryScore'],company['cityScore']]
			writer.writerow(rowdata)



# with open('city.json','r') as f:
# 	cities = json.load(f)

# with open('companies.txt','r') as f:
# 	data = f.readline()
# companies = json.loads(data)

# city_col.insert(cities)
# com_col.insert_one(companies)
# print(type(companies))
# print(companies)
# col = myclient.lagoudb.company_smr
# find_a_com = col.find_one({'result':{'companyShortName':'十点读书'}})
# find_a_com = col.find_one({'totalCount':''})
# cursor = col.find()

# print(col.delete_one({'pageNo':1}))
# print(cursor[0])
# print(find_a_com)

# d = {"pageSize":16,"start":"1424","result":[],"totalCount":"52161","pageNo":90}
# if not d['result']:
# 	print(1)
# else:
# 	print(0)
# def a(city,**pn):
# 	if pn == None:
# 		pn = 100
# 	else:
# 		pn = pn['pn']
# 	print(pn)

# a('123',pn=50)

