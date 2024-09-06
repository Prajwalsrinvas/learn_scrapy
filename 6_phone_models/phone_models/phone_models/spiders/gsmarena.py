from phone_models.items import PhoneModelsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule


class GsmarenaSpider(CrawlSpider):
    name = "gsmarena"
    allowed_domains = ["gsmarena.com"]
    start_urls = ["https://www.gsmarena.com/makers.php3"]
    rules = [
        Rule(
            LinkExtractor(restrict_xpaths=['//div[@class="st-text"]']),
            callback="parse",
            follow=True,
        ),
        Rule(
            LinkExtractor(restrict_xpaths=['//div[@class="makers"]']),
            callback="parse",
            follow=True,
        ),
    ]

    def parse(self, response):
        item = ItemLoader(item=PhoneModelsItem(), response=response, selector=response)
        item.add_xpath("title", '//h1[@data-spec="modelname"]/text()')
        item.add_xpath("date_announced", '//td[@data-spec="year"]/text()')
        yield item.load_item()
