# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company =scrapy.Field()
    category =scrapy.Field()
    value =scrapy.Field()
    main_context =scrapy.Field()

class RateItem(scrapy.Item):
    company = scrapy.Field()
    good = scrapy.Field()
    normal = scrapy.Field()
    bad = scrapy.Field()

class JobItem(scrapy.Item):
    company = scrapy.Field()
    job = scrapy.Field()
    category = scrapy.Field()
    value = scrapy.Field()
    main_context = scrapy.Field()

    pass
