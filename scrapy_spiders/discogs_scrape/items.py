# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DiscogsScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    for_sale = scrapy.Field()
    contributed = scrapy.Field()
    in_collection = scrapy.Field()
    in_wantlist = scrapy.Field()
    images = scrapy.Field()
    reviews = scrapy.Field()
    lists = scrapy.Field()
    username = scrapy.Field()

class UserItem(scrapy.Item):
        username = scrapy.Field()
        coll_release_ids = scrapy.Field()
        want_release_ids = scrapy.Field()
