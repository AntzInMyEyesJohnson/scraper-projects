from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from stack.items import InfluencerItem
# from collections import deque


class InfluencerSpider(CrawlSpider):
    name = "spyballot"
    allowed_domains = ["www.ballotpedia.org"]
    start_urls = ["https://www.ballotpedia.org/Influencers_by_type"]

    rules = (
        Rule(LinkExtractor(allow="https://www.ballotpedia.org/Influencers_by_type"),
             callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        table_list = response.xpath('//table')[0:22]
        while len(table_list) > 0:
            table = table_list.pop()
            itypeh2 = table.xpath('.//preceding::h2[1]/span/text()').extract()[0]
            itypeh3 = table.xpath('.//preceding::h3[1]/span/text()').extract()
            item_name = table.xpath('.//tr//li/a/text()').extract()
            while len(item_name) > 0:
                item = InfluencerItem()
                item['inftype'] = itypeh2 if itypeh2 != "Political leaning" else itypeh3
                item['infname'] = item_name.pop()
                
                yield item
