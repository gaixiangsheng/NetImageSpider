# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NetimagespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    referer = scrapy.Field()
    dir_name = scrapy.Field()
    name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
