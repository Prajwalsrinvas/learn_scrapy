# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join


class SplashQuotesItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field(output_processor=Join())
    quote = scrapy.Field(
        input_processor=lambda x: x[0].strip("\u201c").strip("\u201d"),
        output_processor=Join(),
    )
