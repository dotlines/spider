#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zengls on 2017/11/15
from pymongo import MongoClient

connection = MongoClient('mongodb://localhost:27017/')
db = connection.test_db
collection = db.test_collection
my_dict1 = {'name':"李白", "age":"30", "skill":"Python"}
my_dict2 = {'name':'Lucy', 'sex':'female','job':'nurse'}
collection.remove({})
collection.insert(my_dict1)
collection.insert(my_dict2)

result = collection.find()
print(result)

if __name__ == '__main__':
    pass
