#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/4/29 16:11 
# @Author : zhao.jia
# @Site :  
# @File : zhilianspider.py 
# @Software: PyCharm

import scrapy
import json
from spider_work.items import ZhaopingItem
import re


class ZhaopinSpider(scrapy.Spider):
    name = 'job_spider'
    baseUrl = 'https://fe-api.zhaopin.com/c/i/sou?start={0}&pageSize=90&cityId=489&kw={1}&kt=3'

    offset = 0  # 偏移量

    def start_requests(self):

        with open('keywords.json', 'r', encoding='utf8') as f:
            keywords_list = json.load(f)

        start_urls = []

        for item in keywords_list:
            for key, value in item.items():
                for job_key in value:
                    print(job_key)
                    start_urls.append(self.baseUrl.format(str(self.offset), job_key))

        if start_urls is not None:
            for url in start_urls:
                print("start_url:", url)
                yield scrapy.Request(url=url, callback=self.parse, meta={'start_url': url})

    def parse(self, response):
        '''
        页面解析函数
        :param response:
        :return:
        '''
        data_list = json.loads(response.body)['data']['results']

        if len(data_list) == 0:
            return

        for data in data_list:
            item = ZhaopingItem()
            item["jobType"] = data['jobType']['display']  # 职位所属种类
            item["jobName"] = data['jobName']  # 职位名称
            item["emplType"] = data['emplType']  # 工作类型(兼职、全职)
            item["eduLevel"] = data['eduLevel']['name']  # 学历要求
            item["companyName"] = data['company']['name']  # 公司名称
            item["salary"] = data['salary']  # 薪资
            item["welfare"] = ','.join(data['welfare'])  # 员工福利
            item["city"] = data['city']['display']  # 工作城市
            item["workingExp"] = data['workingExp']['name']  # 工作经验
            # item['infoComLink']=data['company']['url']     #公司详情连接
            # item['positionUrl']=data['positionURL']        # 职位详情链接

            yield item
        init_url = response.meta['start_url']
        self.offset += 90
        str_offset = str(self.offset)
        pattern = 'start=(.*?)&'
        replace_str = 'start=' + str_offset + '&'
        url = re.sub(pattern=pattern, repl=replace_str, string=init_url)
        yield scrapy.Request(url=url, callback=self.parse)
