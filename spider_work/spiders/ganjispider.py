#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/5/5 16:47 
# @Author : zhao.jia
# @Site :  
# @File : ganjispider.py 
# @Software: PyCharm

import scrapy
from spider_work.items import ZhaopingItem
import json


class Jobs58Spider(scrapy.Spider):
    name = 'jobsganjispider'
    allowed_domains = ['ganji.com']
    base_url = 'http://bj.ganji.com/zhaopin/s/_{0}/'
    headers = {
        'Host': 'bj.ganji.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    }
    with open('keywords.json', 'r', encoding='utf8') as f:
        keywords_list = json.load(f)
    pn = 2
    start_urls = []

    for item in keywords_list:
        for key, value in item.items():
            for job_key in value:

                start_urls.append(base_url.format(job_key))

    def start_requests(self):
        if self.start_urls is not None:
            for url in self.start_urls:
                yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        work_href = response.xpath('//div[@class="fl j-title"]/a/@href').extract()
        for i in range(len(work_href)):
            self.headers['Referer'] = 'http://bj.ganji.com/zhaopin/s/_java/?from=zhaopin_indexpage'
            yield scrapy.Request('http://bj.ganji.com' + work_href[i], callback=self.parse_content,
                                 headers=self.headers, dont_filter=True)
        next_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_url:
            yield scrapy.Request('http://bj.ganji.com' + next_url, callback=self.parse)

    def parse_content(self, response):
        item = ZhaopingItem()
        job_type = response.xpath('//div[@class="title-line clearfix"]/h2/text()').extract_first()
        job_name = response.xpath('//div[@class="title-line clearfix"]/p/text()').extract_first()
        salary = response.xpath('//div[@class="salary-line"]/b/text()').extract_first()
        city = response.xpath('//div[@class="location-line clearfix"]/p/text()').extract_first().split('-')[0].strip()
        welfares = response.xpath('//ul[@class="welfare-line clearfix"]/li/span/text()').extract()
        welfare_list = list()
        if not welfares:
            welfare = '无'
        else:
            for w in welfares:
                welfare_list.append(w)
            welfare = ','.join(welfare_list)
        companyName = response.xpath('//div[@class="company-info"]/h3/a/text()').extract_first()
        description = response.xpath('//div[@class="description-label"]/span/text()').extract()
        for i in description:
            if '学历' in i:
                eduLevel = i
            else:
                eduLevel = '不限'
            if '经验' in i:
                workingExp = i
            else:
                workingExp = '不限'
        emplType = '全职'
        item['jobType'] = job_type  # 职位所属种类
        item['jobName'] = job_name  # 职位名称
        item['emplType'] = emplType  # 工作类型(兼职、全职)
        item['eduLevel'] = eduLevel  # 学历要求
        item['companyName'] = companyName  # 公司名称
        item['salary'] = salary  # 薪资
        item['welfare'] = welfare  # 员工福利
        item['city'] = job_name  # 工作城市
        item['workingExp'] = workingExp  # 工作经验
        yield item
