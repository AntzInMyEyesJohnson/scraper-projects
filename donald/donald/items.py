# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class DonaldItem(Item):
    cmtlink = Field()
    title = Field()
    date = Field()
    vote = Field()
    vote_percent = Field()


class SubscriberItem(Item):
    subscriber = Field()
    subandcount = Field()


class CommenterItem(Item):
    cmtlink = Field()
    commenters = Field()
    date = Field()
    # counttest = Field()
    # subscriber = Field()


class WikiResidentItem(Item):
    name = Field()
    hasResidence = Field()


class InfluencerItem(Item):
    infname = Field()
    inftype = Field()
