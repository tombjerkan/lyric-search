import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class SongItem(scrapy.Item):
    artist = scrapy.Field()
    title = scrapy.Field()


def remove_lyrics_ending(title):
    if title[-len(' Lyrics'):] == ' Lyrics':
        return title[:-len(' Lyrics')]
    else:
        return title


class SongItemLoader(scrapy.loader.ItemLoader):
    def __init__(self, **kwargs):
        super().__init__(item=SongItem(), **kwargs)

    artist_in = MapCompose(lambda s: s.strip())
    artist_out = TakeFirst()

    title_in = MapCompose(lambda s: s.strip(), remove_lyrics_ending)
    title_out = TakeFirst()