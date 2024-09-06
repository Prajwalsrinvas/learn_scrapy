# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join


class MediumItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor=Join())
    excerpt = scrapy.Field(output_processor=Join())
    link = scrapy.Field(output_processor=Join())
