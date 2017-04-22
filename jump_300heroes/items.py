# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Player(scrapy.Item):
    name = scrapy.Field()
    level = scrapy.Field()
    win = scrapy.Field()
    match_count = scrapy.Field()
    update_time = scrapy.Field()
    rank = scrapy.Field()
    strength = scrapy.Field()


class ResultList(scrapy.Item):
    name = scrapy.Field()
    match_id = scrapy.Field()
    hero = scrapy.Field()
    result = scrapy.Field()
    date = scrapy.Field()


class GameResult(scrapy.Item):
    match_id = scrapy.Field()
    kill = scrapy.Field()
    death = scrapy.Field()
    support = scrapy.Field()
    score = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    head = scrapy.Field()
