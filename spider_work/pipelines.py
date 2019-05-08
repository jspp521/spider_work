# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from spider_work.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD
from spider_work.items import ZhaopingItem, KeyWordItem
from scrapy import log


class SpiderWorkPipeline(object):

    """
    存储数据
    """
    pass
    # def __init__(self):
    #     # 连接数据库
    #     self.connect = pymysql.connect(
    #         host=MYSQL_HOST,
    #         db=MYSQL_DBNAME,
    #         user=MYSQL_USER,
    #         passwd=MYSQL_PASSWD,
    #         # charset='utf8',
    #         use_unicode=True)
    #
    #     # 通过cursor执行增删查改
    #     self.cursor = self.connect.cursor()
    #
    # def _process_work(self, item):
    #     """
    #     存储用户信息
    #     """
    #     self.connect.ping(reconnect=True)
    #     try:
    #
    #         # 插入数据
    #         sql = """insert into zhihu_user(nickname,zhihu_id, gender, image_url, location, business, employment,
    #             position, education, school_name, major, followee_count, follower_count)
    #             values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s);""" % \
    #               (pymysql.escape_string(item['nickname']),
    #                pymysql.escape_string(item['zhihu_id']),
    #                item['gender'],
    #                pymysql.escape_string(item['image_url']),
    #                pymysql.escape_string(item['location']),
    #                pymysql.escape_string(item['business']),
    #                pymysql.escape_string(item['employment']),
    #                pymysql.escape_string(item['position']),
    #                pymysql.escape_string(item['education']),
    #                pymysql.escape_string(item['school_name']),
    #                pymysql.escape_string(item['major']),
    #                item['followee_count'],
    #                item['follower_count']
    #                )
    #
    #         self.cursor.execute(sql)
    #         # 提交sql语句
    #         self.connect.commit()
    #         print('插入数据成功')
    #     except pymysql.err.ProgrammingError as error:
    #         # 出现错误时打印错误日志
    #         log.logger.error('保存用户时出错' + str(error))
    #     except pymysql.err.InterfaceError as error:
    #         log.logger.error('数据连接已断掉，正在重连。。。')
    #         self.__init__()
    #         self.process_item(item, "zhihu")
    #     except Exception as e:
    #         log.logger.error('保存用户时出错' + str(e))
    #
    # def _process_relation(self, item):
    #     """
    #     存储人际拓扑关系
    #     """
    #     self.connect.ping(reconnect=True)
    #     try:
    #         select_sql = """select user_list from focus where (zhihu_id='%s' and user_type=%d);""" % \
    #                      (item['zhihu_id'], item['user_type'])
    #         self.cursor.execute(select_sql)
    #         old_list = self.cursor.fetchall()
    #         if not old_list:
    #             print('插入user_list')
    #             # 插入数据
    #             self.cursor.execute("""insert into focus(zhihu_id,user_list,user_type) values(%s, %s, %s);""",
    #                                 (item['zhihu_id'], item['user_list'], item['user_type']))
    #             # 提交sql语句
    #             self.connect.commit()
    #         else:
    #
    #             # 数据库中的user_list
    #             old_list = old_list[0][0].split(',')
    #             # item中的user_list
    #             new_list = item['user_list'].split(',')
    #             if old_list != new_list:
    #                 print('两个userlist不一样,update')
    #                 print(item['zhihu_id'])
    #                 # new_list = list(set(old_list) | set(new_list))
    #                 # 两个列表相加，通过set去重，再转为list
    #                 new_list = list(set(old_list + new_list))
    #                 user_list = ','.join(new_list)
    #                 # 更新
    #                 update_sql = """UPDATE focus SET user_list = '%s' WHERE (zhihu_id='%s' and user_type=%s);""" % \
    #                              (user_list, item['zhihu_id'], item['user_type'])
    #                 # 更新
    #                 self.cursor.execute(update_sql)
    #                 # 提交sql语句
    #                 self.connect.commit()
    #             else:
    #                 print('一样')
    #                 pass
    #     except pymysql.err.ProgrammingError as error:
    #         # 出现错误时打印错误日志
    #         log.logger.error('存储人际关系出错' + str(error))
    #         self.connect.rollback()
    #     except pymysql.err.InterfaceError as error:
    #         log.logger.error('数据连接已断掉，正在重连。。。')
    #         self.__init__()
    #         self.process_item(item, "zhihu")
    #     except Exception as e:
    #         log.logger.error('插入数据出错' + str(e))
    #
    # def process_item(self, item, spider):
    #     """
    #     处理item
    #     """
    #     if isinstance(item, ZhihuPeopleItem):
    #         self._process_people(item)
    #     elif isinstance(item, ZhihuRelationItem):
    #         self._process_relation(item)
    #     return item


