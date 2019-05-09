#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/4/29 23:15 
# @Author : zhao.jia
# @Site :  
# @File : process_item_mysql.py 
# @Software: PyCharm

import pymysql
import redis
import json


def process_item(key):
    Redis_conn = redis.StrictRedis(host='ip', port=6379, db=0, password='pass')
    MySql_conn = pymysql.connect(host='ip', user='root', passwd='pass', port=3306, db='dbname')
    cur = MySql_conn.cursor()
    while True:
        data = Redis_conn.lpop(key)
        if data:
            try:
                data = json.loads(data.decode('unicode_escape'), strict=False)
            except Exception as e:
                process_item(key)
            print(data)
            try:
                if '-' in data['city']:
                    city = data['city'].split('-')[0]
                else:
                    city = data['city']
            except Exception as e:
                city = data['city']
            lis = (
                pymysql.escape_string(data['jobType']),
                pymysql.escape_string(data['jobName']),
                pymysql.escape_string(data['emplType']),
                pymysql.escape_string(data['eduLevel']),
                pymysql.escape_string(data['salary']),
                pymysql.escape_string(data['companyName']),
                pymysql.escape_string(city),
                pymysql.escape_string(data['welfare']),
                pymysql.escape_string(data['workingExp']))
            sql = (
                    "replace into work(jobType, jobName, emplType, eduLevel, salary, companyName, city, welfare, workingExp) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % lis)
            try:
                cur.execute(sql)
                MySql_conn.commit()
            except Exception as e:
                MySql_conn.rollback()
        else:
            break
    cur.close()
    MySql_conn.close()


if __name__ == "__main__":
    key_list = ['job_spider:items', 'jobs58:items', 'jobsganjispider']
    for i in range(3):
        process_item(key_list[i])
