import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class SongItem(scrapy.Item):
    artist = scrapy.Field()
    title = scrapy.Field()


class SongItemLoader(scrapy.loader.ItemLoader):
    def __init__(self, **kwargs):
        super().__init__(item=SongItem(), **kwargs)

    artist_in = MapCompose(lambda s: s.strip())
    artist_out = TakeFirst()

    title_in = MapCompose(lambda s: s.strip())
    title_out = TakeFirst()
