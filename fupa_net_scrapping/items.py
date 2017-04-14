# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Player(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    firstName = scrapy.Field()
    lastName = scrapy.Field()
    playerId = scrapy.Field()
    playerUrl = scrapy.Field()
    playerUrlShort = scrapy.Field()
    clubName = scrapy.Field()
    clubImageUrl = scrapy.Field()
    #position = scrapy.Field()
    pass
