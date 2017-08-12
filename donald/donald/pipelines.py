# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging

from scrapy.conf import settings
from scrapy.exceptions import DropItem


class OrganizePipeline(object):

    def __init__(self):
        self.subs = set()
        self.dupe_count = 0
        self.keysub = ''
        # self.count = 0
        # self.error = "ERROR_BELIEVE_IT"

    def process_item(self, item, spider):
        if spider.name == "spysubs":
            self.keysub = item['subscriber']
            item['subandcount'] = {}
            if self.keysub not in self.subs:
                item['subandcount'].setdefault(self.keysub, 1)
                self.subs.add(item['subscriber'])
                logging.info("Subscriber Count: %s" % len(self.subs))
                return item
            else:
                item['subandcount'][self.keysub] += 1
                return item
            self.dupe_count += 1
            # raise DropItem("Subscriber Previously Recorded. Dupe Count: %s" % self.dupe_count)
        elif spider.name is "spyballot":
            item['inftype'] = item['inftype'].capitalize().replace(',', '').replace('.', '')
            item['infname'] = item['infname'].replace(',', '').replace('.', '')
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if spider.name == "spysubs":
            # if item["commenters"] == 'ALREADY RECORDED SUBSCRIBER':
            #     raise DropItem("Duplicate subscriber!")
            return item
            # if item["commenters"] == 'ERROR_BELIEVE_IT':
            #     raise DropItem("Duplicate subscriber!")
        else:
            if str(item['cmtlink']) in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.ids_seen.add(str(item['cmtlink']))
        return item


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if not item:
            raise DropItem('No Item Data!')
        for data in item:
            if not data:
                raise DropItem("Missing data!")
            self.collection.update(
                {'subscriber': item['subscriber']}, dict(item), upsert=True)

        logging.info("Post added to MongoDB database")
        return item
