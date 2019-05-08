#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/4/29 16:13 
# @Author : zhao.jia
# @Site :  
# @File : keyword.py 
# @Software: PyCharm

import scrapy
import json
from spider_work.items import KeyWordItem


class KeyWordSpiderSpider(scrapy.Spider):
    name = 'keywords_spider'
    allowed_domains = ['www.zhaopin.com/']
    start_urls = ['https://www.zhaopin.com/']

    def parse(self, response):
        key_word = list()
        for items in response.xpath('//*[@id="root"]/div[2]/div[2]/div[1]/ol/li'):
            items.xpath('./div[1]/text()').extract_first()
            Industy_name = items.xpath('./div[1]/text()').extract_first()
            Job_keywords = items.xpath('./div[2]/div/div[position()>1]/a/text()').extract()
            if Industy_name == None:
                continue
            # item = KeyWordItem()
            # item['Industy_name'] = items.xpath('./div[1]/text()').extract_first()  # 获取行业名称
            # item['Job_keywords'] = items.xpath('./div[2]/div/div[position()>1]/a/text()').extract()  # 获取职位关键字
            key_word.append({Industy_name: Job_keywords})
            # yield item
        with open('keywords.json', 'w', encoding='utf8') as f:
            json.dump(key_word, f, ensure_ascii=False)