#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zengls on 2017/11/18
from pymongo import MongoClient
import pandas as pd

connection = MongoClient()
# db = connection.get_database('taobao')
# collection = db.products
# for item in collection.find({},{'_id':0,'title':1,'price':1}):
#     print(item)

def get_data_from_db(db,collection):
    db = connection.get_database(db)
    collection = db.get_collection(collection)
    data = collection.find({},{'_id':0,'title':1,'catalogue':1,'price':1,'deal':1,'location':1,'shop':1})
    print('共获取%s条数据.'%str(data.count()))
    return data
if __name__ == '__main__':
    data = get_data_from_db('taobao','products')
    items = []
    for item in data:
        items.append([item['title'],item['catalogue'],item['price'],int(item['deal'][:-3]),item['shop'],item['location']])
    columns = ['品名', '品类', '价格', '销量', '店名', '城市']
    df = pd.DataFrame(items,columns=columns)
    df = df.sort_values('销量',ascending=False)
    df.to_csv('C:/Users/Adam/Desktop/taobao.csv',encoding='utf-8-sig')
    # print(df.head())