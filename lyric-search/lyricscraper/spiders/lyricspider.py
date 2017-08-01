import copy
import scrapy
import string

from lyricscraper.items import SongItem, SongItemLoader


class LyricSpider(scrapy.Spider):
    """Crawls and extracts data for songs from the MetroLyric website.

    A Scrapy spider which finds the lyric pages for all songs on the
    MetroLyrics website and extracts the required data for each song. The data
    is put in SongItem objects which are then passed through the Scrapy
    pipelines.
    """

    # The name of the spider used to identify it when executing Scrapy.
    name = 'lyricspider'

    # The pages on which to start the crawling process.
    start_urls = ['http://www.metrolyrics.com/artists-{}.html'.format(letter)
                  for letter in string.ascii_lowercase]

    def parse(self, response):
        """Parses the artist list pages.

        The links to artists on the page are followed and then the link to the
        next page in the artist list is followed until all pages handled.
        """
        artist_selector = '//table[@class="songs-table"]/tbody/tr/td/a/@href'
        for artist_link in response.xpath(artist_selector):
            yield response.follow(artist_link, callback=self._artist_parse)

        next_page_link = response.css('.next::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

    def _artist_parse(self, response):
        """Parses the song list pages for artists.

        The links to the artist's songs on the page are followed and then the
        link to the next page in the song list is followed until all pages
        handled.

        Extracts the artist name from the page so that it can be assigned to
        songs.
        """
        loader = SongItemLoader(SongItem(), response)
        loader.add_css('artist', '.artist-header h1 ::text')
        song_item = loader.load_item()

        song_selector = '#popular .songs-table a::attr(href)'
        song_links = response.css(song_selector).extract()
        for song_link in song_links:
            yield response.follow(song_link, callback=self._song_parse,
                                  meta={'song_item': copy.deepcopy(song_item)})

        next_page_link = response.css('.next::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self._artist_parse)

    def _song_parse(self, response):
        """Extracts the song title and lyrics from a song's page."""
        song_item = response.meta['song_item']
        loader = SongItemLoader(item=song_item, response=response)
        loader.add_css('title', '.banner-heading h1::text')
        loader.add_css('lyrics', '.verse::text')
        yield loader.load_item()
