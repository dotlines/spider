# -*- coding: utf-8 -*-
import scrapy

class JDSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = ['https://search.jd.com/Search?keyword=%E5%B0%8F%E7%B1%B36&enc=utf-8&suggest=2.def.0.V18&wq=%E5%B0%8F%E7%B1%B3&pvid=2d648233154244758650a8ce3200c7b4']

    def parse(self, response):
        print(len(response.xpath("//li[@class='gl-item']")))

