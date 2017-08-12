# # -*- coding: utf-8 -*-
# # from scrapy import Spider
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from scrapy.http import Request
# from donald.items import SubscribersItem
# import datetime


# class TotalSubscribersSpider(CrawlSpider):
#     name = "wikihunt"
#     allowed_domains = ["reddit.com"]
#     start_date = 1435363200
#     end_date = 1450000000
#     page_count = 0
#     start_string = "https://www.reddit.com/r/The_Donald/search?q=timestamp%%3A%s..%s&sort=new&restrict_sr=on&t=all&syntax=cloudsearch" % (
#         start_date, end_date)
#     start_urls = [start_string]

#     rules = [
#         Rule(LinkExtractor(
#             restrict_xpaths='//a[@rel="nofollow next"]/@href'), follow=True),
#         Rule(LinkExtractor(allow=['\/r\/The_Donald\/comments\/\w*\/\w*\/(|\?ref=search_posts)']),
#              callback='parse_comment_page',
#              follow=True)
#     ]

#     def parse_item(self, response):
#         selector_list = response.css('div.search-result')
#         for selector in selector_list:
#             item_link = {}
#             item_link['cmtlink'] = selector.xpath(
#                 'div/div[contains(@class, "search-result-meta")]/a[contains(@class, "search-comments ")]/@href').extract()
#             item_link['date'] = selector.xpath(
#                 'div/div[contains(@class, "search-result-meta")]/span[contains(@class, "search-time")]/time/@title').extract()
#             item_link['counttest'] = self.page_count

#             request = Request(item_link['cmtlink'][
#                               0], callback=self.parse_comment_page)
#             request.meta['item_link'] = item_link
#             yield request

#     def parse_comment_page(self, response):
#         #item_link = response.meta['item_link']
#         page_link = response.css('div.thing_t3')
#         item_link = {}
#         item_link['date'] = page_link.xpath('//@data-timestamp').extract()
#         item_link['cmtlink'] = page_link.xpath('//@data-url').extract()
#         item_link['counttest'] = 0
#         selector_list = response.css('div.thing, div._thing')
#         for selector in set(selector_list):
#             item = SubscribersItem()
#             item['commenters'] = selector.xpath('//@data-author').extract()
#             item['date'] = item_link['date']
#             item['cmtlink'] = item_link['cmtlink']
#             item['counttest'] = item_link['counttest']
#             yield item

#     def restart_search(startdate, enddate):
#         start_date = startdate
#         end_date = enddate
#         url_string = "https://www.reddit.com/r/The_Donald/search?q=timestamp%%3A%s..%s&sort=new&restrict_sr=on&t=all&syntax=cloudsearch" % (
#             start_date, end_date)
#         return url_string
