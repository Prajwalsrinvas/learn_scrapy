# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from datetime import date

import scrapy
from itemloaders.processors import Join, MapCompose
from w3lib.html import remove_tags


def date_out(val):
    val /= 1000
    return str(date.fromtimestamp(val))


class NaukriItem(scrapy.Item):
    # define the fields for your item here like:
    search_keyword = scrapy.Field(output_processor=Join())
    title = scrapy.Field(output_processor=Join())
    company_name = scrapy.Field(output_processor=Join())
    job_description = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip), output_processor=Join()
    )
    date = scrapy.Field(output_processor=MapCompose(date_out))
    location = scrapy.Field(output_processor=Join())
