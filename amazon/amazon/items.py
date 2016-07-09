# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    numreviews = scrapy.Field()
    item_weight = scrapy.Field()
    item_origin = scrapy.Field()
    item_ASIN = scrapy.Field()
    item_rank = scrapy.Field()
    review_stars = scrapy.Field()
    amazon_category = scrapy.Field()