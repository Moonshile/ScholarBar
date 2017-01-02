# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScholarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    publisher = scrapy.Field()
    authors = scrapy.Field()
    affiliation = scrapy.Field()
    citation_count = scrapy.Field()
    link = scrapy.Field()
    download_link = scrapy.Field()