import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class SongItem(scrapy.Item):
    """Contains data for scraped songs."""

    artist = scrapy.Field()
    title = scrapy.Field()
    lyrics = scrapy.Field()


def remove_lyrics_ending(title):
    """Removes the suffix from the title of lyrics.

    Song titles on MetroLyrics are of the form 'X Lyrics', where X is the name
    of the song. To get just the song name, the ' Lyrics' suffix must be
    removed.
    """
    if title[-len(' Lyrics'):] == ' Lyrics':
        return title[:-len(' Lyrics')]
    else:
        return title


class SongItemLoader(scrapy.loader.ItemLoader):
    """Loads fields for SongItem objects.

    The fields are processed when being assigned to a SongItem object and when
    being used.
    """

    artist_in = MapCompose(lambda s: s.strip())
    artist_out = TakeFirst()

    title_in = MapCompose(lambda s: s.strip(), remove_lyrics_ending)
    title_out = TakeFirst()

    lyrics_in = MapCompose(lambda s: s.strip(), lambda s: s.lower())
    lyrics_out = Join(' ')
