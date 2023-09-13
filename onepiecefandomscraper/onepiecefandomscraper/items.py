# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OnepiecefandomscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


class OnePieceCharacterItem(scrapy.Item):
    name = scrapy.Field()
    episode = scrapy.Field()
    chapter = scrapy.Field()
    year = scrapy.Field()
    note = scrapy.Field()
    appearance = scrapy.Field()
    personality = scrapy.Field()
    abilities_and_powers = scrapy.Field()
