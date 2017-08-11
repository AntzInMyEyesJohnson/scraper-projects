# from scrapy import CrawlSpider
# from scrapy.selector import Selector

# from stack.items import StackItem


# class StackSpider(CrawlSpider):
#     name = "spystack"
#     allowed_domains = ["ballotpedia.org"]
#     start_urls = [
#     "https://ballotpedia.org/National_influencers",
#     ]

#     def parse(self, response):
#         selector_list = response

#         for question in questions:
#             item = StackItem()
#             item['title'] = question.xpath('a[@class="question-hyperlink"]/text()').extract()[0]
#             item['url'] = question.xpath('a[@class="question-hyperlink"]/@href').extract()[0]
#             yield item
