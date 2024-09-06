from classifieds.items import ClassifiedsItem
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule


class ClickInSpider(CrawlSpider):
    name = "click_in"
    allowed_domains = ["click.in"]
    rules = [
        Rule(
            LinkExtractor(restrict_xpaths='//div[@id="classifieds_list"]'),
            callback="parse",
            process_request="add_meta",
            # follow=True,
        )
    ]

    def add_meta(self, request, response):
        # https://docs.scrapy.org/en/latest/topics/spiders.html?highlight=process_request#crawling-rules
        request.meta["impersonate"] = "chrome110"
        return request

    def start_requests(self):
        url = "https://www.click.in/used-cars-ctgid48"
        yield Request(url=url, meta={"impersonate": "chrome110"})

    def parse(self, response):
        item = ItemLoader(item=ClassifiedsItem(), response=response, selector=response)
        item.add_xpath("title", '//h1[@class="clickin-post-title"]/text()')
        item.add_xpath(
            "locality",
            '//td[div="Locality "]/div[@class="clickin-post-blackbold"]/text()',
        )
        item.add_xpath(
            "address", '//div[div="Address"]/div/p[@class="clickin-desc-text"]/text()'
        )
        item.add_xpath(
            "landline",
            '//div[div="Landline"]/div[@class="clickin-post-blackbold"]/text()',
        )
        item.add_xpath(
            "mobile", '//div[div="Mobile"]/div[@class="clickin-post-blackbold"]/text()'
        )
        item.add_xpath(
            "description",
            '//div[@class="clickin-description"]//p[@class="clickin-desc-text"]/text()',
        )
        item.add_xpath(
            "price", '//td[div="Price"]/div[@class="clickin-post-blackbold"]/text()'
        )
        yield item.load_item()
