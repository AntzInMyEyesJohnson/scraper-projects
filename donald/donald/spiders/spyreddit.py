# -*- coding: utf-8 -*-
# from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from donald.items import DonaldItem


class RedditSpider(CrawlSpider):
    name = "spyreddit"
    allowed_domains = ["reddit.com"]
    start_urls = [
        'https://www.reddit.com/r/The_Donald/controversial/?sort=controversial&t=month']

    rules = [
        Rule(LinkExtractor(
            allow=['\/r\/The_Donald\/controversial\/\?sort=controversial&t=month',
                   '\/r\/The_Donald\/controversial\/\?sort=controversial&t=month&count=\d*&(after|before)=\w*']),
             callback='parse_item',
             follow=True)
    ]

    def parse_item(self, response):
        selector_list = response.css('div.thing')
        for selector in selector_list:
            item = DonaldItem()
            item['title'] = selector.xpath('div/p/a/text()').extract()
            item['cmtlink'] = selector.xpath(
                'div[contains(@class, "entry ")]/ul/li[contains(@class, "first")]/a/@href').extract()
            item['date'] = selector.xpath(
                'div[contains(@class, "entry ")]/p[contains(@class, "tagline")]/time[@class="live-timestamp"]/@title').extract()
            votecount = selector.xpath(
                'div/div[contains(@class, "score unvoted")]/text()').extract()[0]
            if str(votecount).find('k') != -1:
                votecount = str(votecount).replace(".", "").replace("k", "00")

            item['vote'] = int(votecount)
            # item['absoluteurl'] = selector + item['cmtlink'][0]
            request = Request(item['cmtlink'][0], callback=self.parse_comment_page)
            request.meta['item'] = item
            yield request

    def parse_comment_page(self, response):
        item = response.meta['item']
        vp = response.xpath(
            '//html/body/div[3]/div[2]/div/div[2]/text()').extract()[1]
        item['vote_percent'] = int(vp[2:4])
        return item
