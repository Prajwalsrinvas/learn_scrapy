import scrapy
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
from wikipedia.items import WikipediaItem


class SplashSpider(scrapy.Spider):
    name = "splash"
    allowed_domains = ["www.wikipedia.org"]

    def start_requests(self):
        url = "https://en.wikipedia.org/wiki/Scrapy"
        yield SplashRequest(url=url, callback=self.parse, args={"wait": 1})

    def parse(self, response):
        item = ItemLoader(item=WikipediaItem(), response=response, selector=response)
        item.add_xpath("title", '//h1[@id="firstHeading"]/span/text()')
        item.add_xpath("content", '//div[@class="mw-content-ltr mw-parser-output"]')
        yield item.load_item()
