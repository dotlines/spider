# -*- coding: utf-8 -*-
"""
 @desc:
 @author: adam
 @software: PyCharm on 18-8-19
"""
import pandas as pd
from pymongo import MongoClient
from time import time
from enum import Enum,unique

myclient = MongoClient('127.0.0.1',27017)
mydb = myclient['lagoudb']
posit_col = mydb['position_list']
cursor = posit_col.find()

class Field(Enum):
    companyId = '公司ID'
    positionId = '岗位ID'
    jobNature = '工作性质'
    financeStage = '发展阶段'
    companyName = '公司简称'
    companyFullName = '公司全称'
    companySize = '公司规模'
    industryField = '领域'
    positionName = '岗位名称'
    city = '工作城市'
    createTime = '发布时间'
    salary = '工资'
    workYear = '工作年限'
    education = '教育水平'
    positionAdvantage = '职位诱惑'
    companyLabelList = '公司标签'
    userId = '用户ID'
    companyLogo = '公司logo'
    haveDeliver = ''
    score = ''
    adWord = ''
    adTimes = ''
    adBeforeDetailPV = ''
    adAfterDetailPV = ''
    adBeforeReceivedCount = ''
    adAfterReceivedCount = ''
    isCalcScore = ''
    searchScore = ''
    district = '城区'
    positionUrl = '岗位链接'
    companyUrl = '公司链接'

posit_count = 0
company_count = 0
position_list = []
posit_field = [Field.positionName, Field.companyName, Field.companyFullName, Field.positionUrl,
                       Field.companyUrl, Field.jobNature, Field.financeStage, Field.companySize, Field.industryField,
                       Field.city, Field.district, Field.createTime, Field.salary, Field.workYear, Field.education,
                       Field.positionAdvantage, Field.companyLabelList, Field.companyLogo]


# print(posit_data.keys())

start_time = time()

for results in cursor:
    for data in results['allContent']:
        positions = data['content']['data']['page']['result']
        for posit in positions:
            posit_data = {}
            for field in posit_field:
                if field.name == 'positionUrl':
                    posit_data[field.value] = 'https://www.lagou.com/jobs/%d.html'%posit[Field.positionId.name]
                    continue
                if field.name == 'companyUrl':
                    posit_data[field.value] = 'https://www.lagou.com/gongsi/%d.html'%posit[Field.companyId.name]
                    continue
                if field.name == 'district':
                    if 'district' not in posit.keys():
                        posit_data[field.value] = ''
                        continue
                posit_data[field.value] = posit[field.name]
            # print(posit_data)
            posit_count += 1
            position_list.append(posit_data)
    company_count += 1
end_time = time()
print('共 %d 个公司，%d 个岗位，共耗时%.2f秒'%(company_count,posit_count,(end_time-start_time)))
df = pd.DataFrame(position_list,columns=[field.value for field in posit_field])
# print(df)
df.to_csv('lagou_data.csv')
# for po in position_list:
#     print(po)


