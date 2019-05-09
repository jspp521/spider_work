# spider_work

## 关于赶集网job， 58job以及智联招聘的爬虫

该项目框架为scrapy_redis, 使用redis做增量爬取去重，以及存储数据。

## 配置setting

需要配置redis数据库的IP，端口以及密码

## 启动方式

配置了crawlall，可以直接启动所有的爬虫

`scrapy crawlall`

## process_item_mysql.py

这是将redis中的数据文件提取出来去重后存到MySQL数据库中，并继续做进一步的分析处理

## 可视化 flask+mysql+echarts

这一部分的代码没有提交，后续会提交。

![edu](https://github.com/AndrewAndrea/spider_work/blob/master/images/%E6%97%A0%E6%A0%87%E9%A2%98.png)

![wordcloud](https://github.com/AndrewAndrea/spider_work/blob/master/images/%E6%97%A0%E6%A0%87%E9%A2%981.png)

![exp](https://github.com/AndrewAndrea/spider_work/blob/master/images/%E6%97%A0%E6%A0%87%E9%A2%982.png)

![area](https://github.com/AndrewAndrea/spider_work/blob/master/images/%E6%97%A0%E6%A0%87%E9%A2%983.png)

![select](https://github.com/AndrewAndrea/spider_work/blob/master/images/%E6%97%A0%E6%A0%87%E9%A2%984.png)


