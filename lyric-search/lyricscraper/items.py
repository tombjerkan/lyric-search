import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class SongItem(scrapy.Item):
    """Contains data for scraped songs."""

    artist = scrapy.Field()
    title = scrapy.Field()
    lyrics = scrapy.Field()


def remove_lyrics_ending(text):
    """Removes the suffix from the title of artists and songs.

    Artist and song titles on MetroLyrics are of the form 'X Lyrics', where X
    is the name of the artist or song, so this ending must be removed.
    """
    if text[-len(' Lyrics'):] == ' Lyrics':
        return text[:-len(' Lyrics')]
    else:
        return text


class SongItemLoader(scrapy.loader.ItemLoader):
    """Loads fields for SongItem objects.

    The fields are processed when being assigned to a SongItem object and when
    being used.
    """

    artist_in = MapCompose(lambda s: s.strip(), remove_lyrics_ending)
    artist_out = TakeFirst()

    title_in = MapCompose(lambda s: s.strip(), remove_lyrics_ending)
    title_out = TakeFirst()

    lyrics_in = MapCompose(lambda s: s.strip(), lambda s: s.lower())
    lyrics_out = Join(' ')
