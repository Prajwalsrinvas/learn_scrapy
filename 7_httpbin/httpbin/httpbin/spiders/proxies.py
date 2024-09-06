import scrapy


class ProxiesSpider(scrapy.Spider):
    name = "proxies"
    allowed_domains = ["httpbin.org"]
    start_urls = ["https://httpbin.org/ip"]

    def parse(self, response):
        yield response.json()
        yield scrapy.Request(self.start_urls[0], dont_filter=True)
