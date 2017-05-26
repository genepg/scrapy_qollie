# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

from qollie.items import RateItem, CommentItem, JobItem

class QolliePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        # self.cursor = self.connect.cursor()

    @classmethod
    def from_settings(cls, settings):

        dbargs = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            port = settings['MYSQL_PORT'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True,
        )

        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    #pipeline
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return item

    #insert every new page
    def _do_upinsert(self, conn, item, spider):
        if item.__class__ == RateItem:
            valid = True
            for data in item:
                if not data:
                    valid = False
                    # raise DropItem("Missing {0}!".format(data))
                    print ("Missing data")
            if valid:
                result = conn.execute("""
                    insert into qollie_rate(company, good, bad, normal)
                    values(%s, %s, %s, %s)
                    """, (item['company'], item['good'], item['bad'], item['normal']))
                if result:
                    print ("added into db")
                else:
                    print ("failed insert into qollie")
        elif item.__class__ == CommentItem:
            valid = True
            for data in item:
                if not data:
                    valid = False
                    # raise DropItem("Missing {0}!".format(data))
                    print ("Missing data")
            if valid:
                result = conn.execute("""
                    insert into qollie_comment(company, category, value, main_context)
                    values(%s, %s, %s, %s)
                    """, (item['company'], item['category'], item['value'], item['main_context']))
                if result:
                    print ("added into db")
                else:
                    print ("failed insert into qollie")
        elif item.__class__==JobItem:
            valid = True
            for data in item:
                if not data:
                    valid = False
                    # raise DropItem("Missing {0}!".format(data))
                    print ("Missing data")
            if valid:
                result = conn.execute("""
                    insert into qollie_job(company, job, category, value, main_context )
                    values(%s, %s, %s, %s, %s)
                    """, (item['company'], item['job'], item['category'], item['value'], item['main_context']))
                if result:
                    print ("added into db")
                else:
                    print ("failed insert into qollie")
                
        else:
            print("can't find any item")
