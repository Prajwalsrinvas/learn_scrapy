# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose


def clean_description(value_list):
    """
    Cleans the description by removing empty values and reversing the list.

    Args:
        value_list (list): The list of values to be cleaned.

    Returns:
        dict: A dictionary with the cleaned values.
    """
    temp = [i for i in value_list if i][::-1]
    value_list = dict(zip(temp[::2], temp[1::2]))
    return value_list


class RealEstateItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=Join(", ")
    )
    description = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=clean_description
    )
    price = scrapy.Field(output_processor=Join())
    agency = scrapy.Field(output_processor=Join())
