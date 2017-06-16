import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class SongItem(scrapy.Item):
    artist = scrapy.Field()
    title = scrapy.Field()
    lyrics = scrapy.Field()


def remove_lyrics_ending(title):
    if title[-len(' Lyrics'):] == ' Lyrics':
        return title[:-len(' Lyrics')]
    else:
        return title


class SongItemLoader(scrapy.loader.ItemLoader):
    artist_in = MapCompose(lambda s: s.strip())
    artist_out = TakeFirst()

    title_in = MapCompose(lambda s: s.strip(), remove_lyrics_ending)
    title_out = TakeFirst()

    lyrics_in = MapCompose(lambda s: s.strip(), lambda s: s.lower())
    lyrics_out = Join(' ')