# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InputmongodbItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()

    release_date = scrapy.Field()
    developer = scrapy.Field()
    publisher = scrapy.Field()
    summary = scrapy.Field()
    review = scrapy.Field()
    image = scrapy.Field()

    tags = scrapy.Field()
    comments = scrapy.Field()
    pass
