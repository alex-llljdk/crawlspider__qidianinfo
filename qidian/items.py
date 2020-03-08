# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    status = scrapy.Field()
    type = scrapy.Field()
    brief = scrapy.Field()
    contents = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()

