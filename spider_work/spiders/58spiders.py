#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/4/30 9:05 
# @Author : zhao.jia
# @Site :  
# @File : 58spiders.py 
# @Software: PyCharm

import scrapy
from scrapy.http import Request
from spider_work.items import ZhaopingItem
import json


class Jobs58Spider(scrapy.Spider):
    name = 'jobs58'
    allowed_domains = ['58.com']
    city = '西安'
    base_url = 'https://xa.58.com/job/?key={0}&final=1&jump=1'
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
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.xpath('//li[@class="job_item clearfix"]')
        item = ZhaopingItem()
        for i in range(len(items)):
            job_names = items[i].xpath(
                './/div[@class="job_name clearfix"]/a')
            # 工作名称
            job_name = job_names.xpath('string(.)').extract()[0].split('|')[1].strip()
            salary = items[i].xpath(
                './/p[@class="job_salary"]/text()').extract_first()
            welfare = items[i].xpath(
                './/div[@class="job_wel clearfix"]')
            try:
                welfare = welfare.xpath('string(.)').extract_first().strip().replace('   ', ',')
            except Exception as e:
                welfare = '0'
            companyName = items[i].xpath(
                './/div[@class="comp_name"]/a/text()').extract_first().strip()
            job_type = items[i].xpath('.//p[@class="job_require"]/span[@class="cate"]/text()').extract_first()
            eduLevel = items[i].xpath('.//p[@class="job_require"]/span[@class="xueli"]/text()').extract_first()
            workingExp = items[i].xpath('.//p[@class="job_require"]/span[@class="jingyan"]/text()').extract_first()
            emplType = '全职'

            item['jobType'] = job_type  # 职位所属种类
            item['jobName'] = job_name  # 职位名称
            item['emplType'] = emplType  # 工作类型(兼职、全职)
            item['eduLevel'] = eduLevel  # 学历要求
            item['companyName'] = companyName  # 公司名称
            item['salary'] = salary  # 薪资
            item['welfare'] = welfare  # 员工福利
            item['city'] = job_names.xpath('string(.)').extract()[0].split('|')[0].strip()  # 工作城市
            item['workingExp'] = workingExp  # 工作经验
            yield item
        try:

            if response.xpath('//a[@class="iconfont icon_arrow_right hover"]'):
            # while True:
                url_page = 'https://bj.58.com/job/pn{0}/?key=Java&final=1&jump=1&PGTID=0d302408-0000-148c-877f-6822d08c7eee&ClickID=1'.format(str(self.pn))
                yield scrapy.Request(url=url_page, callback=self.parse)
                self.pn += 1
            else:
                self.pn = 2
        except Exception as e:
            print('没有下一页了')





        # print(links)
        # for link in links:
        #     yield Request(link, callback=self.getDetail)
    #
    # def getDetail(self, response):
    #     print('got', response.url, response)
    #     title = response.xpath('//span[@class="pos_title"]/text()')[0].extract()
    #     try:
    #         salary = response.xpath('//span[@class="pos_salary"]/text()')[0].extract()
    #     except:
    #         salary = 0
    #     num = response.xpath('//span[@class="item_condition pad_left_none"]/text()')[0].extract()
    #     edu = response.xpath('//span[@class="item_condition"]/text()')[0].extract()
    #     exp = response.xpath('//span[@class="item_condition border_right_None"]/text()')[0].extract()
    #     area = response.xpath('//span[@class="pos_area_span pos_address"]//a/text()').extract()
    #     # print(title,num,edu,area,exp,salary)
    #     item = ZhaopingItem()
    #     item['title'] = title.strip()
    #     item['salary'] = salary.strip()
    #     item['num'] = num.strip('招人 ')
    #     item['edu'] = edu.strip()
    #     item['exp'] = exp.strip()
    #     item['area'] = area
    #     print(item)
    #     # yield item
