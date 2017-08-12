# # -*- coding: utf-8 -*-
# # from scrapy import Spider
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from scrapy.http import Request
# from donald.items import SubscribersItem
# import datetime


# class TotalSubscribersSpider(CrawlSpider):
#     name = "spysubs"
#     allowed_domains = ["reddit.com"]
#     start_date = 1435363200
#     end_date = 1450000000
#     page_count = 0
#     start_string = "https://www.reddit.com/r/The_Donald/search?q=timestamp%%3A%s..%s&sort=new&restrict_sr=on&t=all&syntax=cloudsearch" % (
#         start_date, end_date)
#     start_urls = [start_string]

#     rules = [
#         Rule(LinkExtractor(
#             allow=["\/r\/The_Donald\/search\?q=timestamp%3A\d*\.\.\d*&sort=new&restrict_sr=on&t=all&syntax=cloudsearch",
#                    "\/r\/The_Donald\/search\?q=timestamp%3A\d*\.\.\d*&sort=new&restrict_sr=on&t=all&syntax=cloudsearch&count=\d*&after=\w*"]),
#              callback='parse_item',
#              follow=True)
#     ]

#     def parse_item(self, response):
#         selector_list = response.css('div.search-result')
#         if len(selector_list) < 25:
#             self.page_count += 1
#             page_date = selector_list[len(selector_list)].xpath(
#                 'div/div[contains(@class, "search-result-meta")]/span[contains(@class, "search-time")]/time/@title').extract()
#             epoch = datetime.datetime.utcfromtimestamp(0)
#             new_start_date = (page_date[0] - epoch).total_seconds() * 1000.0
#             new_link = self.restart_search(new_start_date, new_start_date + 10000000)
#             new_request = Request(new_link, callback=self.parse_item)
#             yield new_request
#         else:
#             for selector in selector_list:
#                 item_link = {}
#                 item_link['cmtlink'] = selector.xpath(
#                     'div/div[contains(@class, "search-result-meta")]/a[contains(@class, "search-comments ")]/@href').extract()
#                 item_link['date'] = selector.xpath(
#                     'div/div[contains(@class, "search-result-meta")]/span[contains(@class, "search-time")]/time/@title').extract()
#                 item_link['counttest'] = self.page_count

#                 request = Request(item_link['cmtlink'][
#                                   0], callback=self.parse_comment_page)
#                 request.meta['item_link'] = item_link
#                 yield request

#     def parse_comment_page(self, response):
#         item_link = response.meta['item_link']
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
