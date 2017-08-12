# -*- coding: utf-8 -*-
# from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from donald.items import SubscriberItem
# import datetime


class TotalSubscribersSpider(CrawlSpider):
    name = "spysubs"
    allowed_domains = ["reddit.com"]
    start_date = 1435363200
    end_date = 1450000000
    page_count = 0
    start_string = "https://www.reddit.com/r/The_Donald/search?q=timestamp%%3A%s..%s&sort=new&restrict_sr=on&t=all&syntax=cloudsearch" % (
        start_date, end_date)
    start_urls = [start_string]

    rules = (
        Rule(LinkExtractor(allow='https://www.reddit.com/r/The_Donald/search\?q=timestamp%3A\d*\.\.\d*&sort=new&restrict_sr=on&t=all&syntax=cloudsearch&count=\d*&after=\w*',
                           restrict_xpaths="//a[@rel='nofollow next']"),
             follow=True),

        Rule(LinkExtractor(allow='https://www.reddit.com/r/The_Donald/comments/\w*/\w*/(|\?ref=search_posts)',
                           restrict_xpaths="//div[@class='search-result-meta']/a"),
             callback='parse_comment_page',
             follow=True)

    )

    def parse_comment_page(self, response):
        selector_list = response.css('div.thing, div._thing')
        for selector in set(selector_list):
            item_set = set(selector.xpath('//@data-author').extract())
            while len(item_set) > 0:
                item = SubscriberItem()
                item['subscriber'] = item_set.pop()
                yield item

    # def restart_search(startdate, enddate):
    #     start_date = startdate
    #     end_date = enddate
    #     url_string = "https://www.reddit.com/r/The_Donald/search?q=timestamp%%3A%s..%s&sort=new&restrict_sr=on&t=all&syntax=cloudsearch" % (
    #         start_date, end_date)
    #     return url_string
