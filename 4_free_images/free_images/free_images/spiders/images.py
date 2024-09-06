from free_images.items import FreeImagesItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule


class ImagesSpider(CrawlSpider):
    name = "images"
    allowed_domains = ["freeimages.com"]

    rules = [
        Rule(
            LinkExtractor(restrict_xpaths=('//div[@class="grid-item"]')),
            callback="parse",
            follow=False,
        )
    ]

    def __init__(self, *args, **kwargs):
        super(ImagesSpider, self).__init__(*args, **kwargs)

        self.start_urls = [f"http://freeimages.com/search/{kwargs.get('category')}"]

    def parse(self, response):
        item = ItemLoader(item=FreeImagesItem(), response=response, selector=response)
        item.add_xpath("image_urls", '//img[@id="photo"]/@src')
        yield item.load_item()
