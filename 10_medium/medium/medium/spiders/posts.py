import time

import scrapy
from medium.items import MediumItem
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from selenium import webdriver


class PostsSpider(scrapy.Spider):
    name = "posts"
    allowed_domains = ["medium.com"]
    start_urls = ["https://medium.com/tag/llm/archive"]

    def parse(self, r):
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(self.start_urls[0])
        driver.implicitly_wait(5)
        i = 1
        num_scrolls = 10
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True and i <= num_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            response = driver.page_source
            selector = Selector(text=response)
            posts = selector.xpath('//div[@class="ks kt ku l"]')
            for post in posts:
                item = ItemLoader(item=MediumItem(), response=response, selector=post)
                item.add_xpath("title", ".//h2/text()")
                item.add_xpath("excerpt", ".//h3/text()")
                item.add_xpath("link", ".//a[h2]/@href")
                yield item.load_item()
            i += 1
        driver.quit()
