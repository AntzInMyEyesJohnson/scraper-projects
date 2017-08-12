# # -*- coding: utf-8 -*-
# #from scrapy import Spider
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from scrapy.http import Request
# from donald.items import DonaldItem


# class RedditSpider(CrawlSpider):
#     name = "spyreddit_old"
#     allowed_domains = ["reddit.com"]
#     start_urls = ['https://www.reddit.com/r/The_Donald/controversial/?sort=controversial&t=all']

#     rules = [
#         Rule(LinkExtractor(
#             allow=['\/r\/The_Donald\/controversial\/\?sort=controversial&t=all', '\/r\/The_Donald\/controversial\/\?sort=controversial&t=all&count=\d*&(after|before)=\w*']),
#             callback='parse_item',
#             follow=True)
#     ]
#     def parse_item(self, response):
#         links = response.xpath(
#             '//p[@class="title"]/a[@class="title may-blank "]/@href').extract()
#         cmtlinks = response.xpath(
#             '//li[@class="first"]/a[@class="bylink comments may-blank"]/@href').extract()
#         titles = response.xpath(
#             '//div[@id="[\w*]"]/div[2]/p[1]/a/text()').extract()
#         # 'p[@class="title"]/a[@class="title may-blank "]/text()').extract()
#         # id('thing_t3_4essp6')/x:div[2]/x:p[1]/x:a
#         # id('thing_t3_4f4b77')/x:div[2]/x:p[1]/x:a
#         dates = response.xpath(
#             '//p[@class="tagline"]/time[@class="live-timestamp"]/@title').extract()
#         votes = response.xpath(
#             '//div[@class="midcol unvoted"]/div[@class="score unvoted"]/text()').extract()

#         for i, clink in enumerate(cmtlinks, start=0):
#             # print("clink {}: {}".format(i, clink))
#             item = DonaldItem()
#             item['cmtlink'] = cmtlinks[i]
#             item['title'] = titles[i]
#             item['date'] = dates[i]
#             # bullet point (ie not enough votes yet or hidden)
#             if votes[i] == u'\u2022':
#                 item['vote'] = 'hidden'
#             else:
#                 item['vote'] = votes[i]

#             request = Request(clink, callback=self.parse_comment_page)
#             request.meta['item'] = item
#             yield request

#     def parse_comment_page(self, response):
#         item = response.meta['item']
#         # print(response.xpath('//html/body/div[3]/div[2]/div/div[2]/text()'))
#         vp = response.xpath(
#             '//html/body/div[3]/div[2]/div/div[2]/text()').extract()[1]
#         item['vote_percent'] = int(vp[2:4])
#         # print(item)
#         yield item
# from __future__ import absolute_import
# import re

# from bs4 import BeautifulSoup
# from scrapy import (Spider, Request)


# class RedditSpider(Spider):
#     name = 'spyreddit'
#     allowed_domains = ['reddit.com', ""]
#     start_urls = ('https://www.reddit.com/r/The_Donald', )

#     def parse(self, response):
#         links = response.xpath(
#             '//p[@class="title"]/a[@class="title may-blank "]/@href').extract()
#         titles = response.xpath(
#             '//p[@class="title"]/a[@class="title may-blank "]/text()').extract()
#         dates = response.xpath(
#             '//p[@class="tagline"]/time[@class="live-timestamp"]/@title').extract()
#         votes = response.xpath(
#             '//div[@class="midcol unvoted"]/div[@class="score unvoted"]/text()').extract()
#         comments = response.xpath(
#             '//div[@id="siteTable"]/a[@class="comments may-blank"]/@href').extract()
#         # import pudb; pudb.set_trace()

#         for i, link in enumerate(comments):
#             item = DonaldItem()
#             item['subreddit'] = str(re.findall('/r/[A-Za-z_]*8?', link))[3]
#             item['link'] = links[i]
#             item['title'] = titles[i]
#             item['date'] = dates[i]
#             # bullet point (ie not enough votes yet or hidden)
#             if votes[i] == u'\u2022':
#                 item['vote'] = 'hidden'
#             else:
#                 item['vote'] = int(votes[i])

#             request = Request(link, callback=self.parse_comment_page)
#             request.meta['item'] = item

#             yield request

#     def parse_comment_page(self, response):
#         item = response.meta['item']

#         item['vote_percent'] = response.xpath(
#             '//html/body/div[3]/div[2]/div/div[2]/text()')

#         yield item