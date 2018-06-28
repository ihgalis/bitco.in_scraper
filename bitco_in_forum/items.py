# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BitcoInForumItem(scrapy.Item):
    author = scrapy.Field()
    datetime = scrapy.Field()
    topic = scrapy.Field()
    posttext = scrapy.Field()
    identityhash = scrapy.Field()
