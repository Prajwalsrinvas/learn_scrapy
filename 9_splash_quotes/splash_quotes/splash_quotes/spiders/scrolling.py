import scrapy
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
from splash_quotes.items import SplashQuotesItem


class ScrollingSpider(scrapy.Spider):
    name = "scrolling"
    allowed_domains = ["quotes.toscrape.com"]
    lua_scroll_script = """
        function main(splash)
            local num_scrolls = 20
            local scroll_delay = 1
            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc("function() {return document.body.scrollHeight;}")
            assert(splash:go(splash.args.url))
            splash:wait(splash.args.wait)

            for _ = 1, num_scrolls do
                local height = get_body_height()
                for i = 1, 10 do
                    scroll_to(0, height * i / 10)
                    splash:wait(scroll_delay / 10)
                end
            end
            return splash:html()
        end
        """

    def start_requests(self):
        url = "https://quotes.toscrape.com/scroll"
        yield SplashRequest(
            url=url,
            callback=self.parse,
            endpoint="execute",
            args={"wait": 1, "lua_source": self.lua_scroll_script},
        )

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            item = ItemLoader(
                item=SplashQuotesItem(), response=response, selector=quote
            )
            item.add_xpath("author", './/small[@class="author"]/text()')
            item.add_xpath("quote", './/span[@class="text"]/text()')
            yield item.load_item()
