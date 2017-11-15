#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zengls on 2017/11/16
import random
from fake_useragent import UserAgent

ua = UserAgent()

for i in range(10):
    print(random.random()*3)
    print(ua.random)
if __name__ == '__main__':
    pass