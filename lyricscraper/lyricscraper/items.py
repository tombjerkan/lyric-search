import scrapy


class SongItem(scrapy.Item):
    artist = scrapy.Field()
    title = scrapy.Field()
