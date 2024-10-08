from real_estate.items import RealEstateItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule


class ListingsSpider(CrawlSpider):
    name = "listings"
    allowed_domains = ["arizonarealestate.com"]
    start_urls = ["https://arizonarealestate.com"]
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=('//section[@class="section-city-list"]')),
            callback="parse",
            follow=True,
        ),
    )

    def parse(self, response):
        gallery = response.xpath('//div[@class="si-listings-column"]')
        for listing in gallery:
            item = ItemLoader(item=RealEstateItem(), response=response)
            item.selector = listing

            item.add_xpath("name", './/div[@class="si-listing__title-main"]/text()')
            item.add_xpath(
                "name", './/div[@class="si-listing__neighborhood"]/span/text()'
            )
            item.add_xpath(
                "description", './/div[@class="si-listing__info"]/div//text()'
            )
            item.add_xpath(
                "price", './/div[@class="si-listing__photo-price"]/span/text()'
            )
            item.add_xpath("agency", './/div[@class="si-listing__footer"]/div/text()')

            yield item.load_item()
            next_page = response.xpath('//a[@class="js-page-link"]/@href').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
