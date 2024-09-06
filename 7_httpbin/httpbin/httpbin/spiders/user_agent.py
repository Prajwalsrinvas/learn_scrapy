import scrapy


class UserAgentSpider(scrapy.Spider):
    name = "user_agent"
    allowed_domains = ["httpbin.org"]
    start_urls = ["https://httpbin.org/user-agent"]

    def parse(self, response):
        yield response.json()
        yield scrapy.Request(self.start_urls[0], dont_filter=True)
