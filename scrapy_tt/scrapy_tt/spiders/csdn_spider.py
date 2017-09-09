# -*- coding:UTF-8 -*-
import scrapy
from scrapy_tt.items import CSDNItem
class CSDNSpider(scrapy.Spider):
	name = 'csdn'
	allowed_domains = ['csdn.net']
	start_urls = ["http://geek.csdn.net/bigdata","http://geek.csdn.net/iot"]

	def parse(self,response):

		# filename = response.url.split('/')[-1] + '.html'
		# with open(filename,'wb') as f:
		# 	f.write(response.body)
		item = CSDNItem()
		geek_lists = response.xpath('//dl[@class=\'geek_list\']/dd')
		for sel in geek_lists:
			item['title'] = sel.xpath('span/a/text()').extract()
			item['link'] = sel.xpath('span/a/@href').extract()
			item['reading_num'] = sel.xpath('ul/li[@class=\'read_num\']/em/text()').extract()
			item['date'] = sel.xpath('ul/li[2]/text()').extract()
			yield item
