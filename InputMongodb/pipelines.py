# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class InputmongodbPipeline(object):
    def __init__(self):

        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client.ScrapyChina

    def process_item(self, item, spider):

        self.db.steamGames.insert(dict(item))
        return item
