# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BallotPipeline(object):
    def process_item(self, item, spider):
        if spider.name is "spyballot":
            item['inftype'] = item['inftype'].capitalize().replace(',', '').replace('.', '')
            item['infname'] = item['infname'].replace(',', '').replace('.', '')
        return item
