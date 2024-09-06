# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


def clean(s):
    return s[0].replace("\t", "").replace("\n", "").replace("\xa0", " ").strip("\t")


class ClassifiedsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor=clean)
    locality = scrapy.Field(output_processor=clean)
    address = scrapy.Field(output_processor=clean)
    landline = scrapy.Field(output_processor=clean)
    mobile = scrapy.Field(output_processor=clean)
    description = scrapy.Field(output_processor=clean)
    price = scrapy.Field(output_processor=clean)
