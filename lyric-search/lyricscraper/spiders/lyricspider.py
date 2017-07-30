import copy
import scrapy
import string

from lyricscraper.items import SongItem, SongItemLoader


class LyricSpider(scrapy.Spider):
    name = 'lyricspider'

    # Starts at the initial page for artists grouped alphabetically
    start_urls = ['http://www.metrolyrics.com/artists-{}.html'.format(letter)
                  for letter in string.ascii_lowercase]

    def parse(self, response):
        artist_selector = '//table[@class="songs-table"]/tbody/tr/td/a/@href'
        for artist_link in response.xpath(artist_selector):
            yield response.follow(artist_link, callback=self._artist_parse)

        next_page_link = response.css('.next::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

    def _artist_parse(self, response):
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
        song_item = response.meta['song_item']
        loader = SongItemLoader(item=song_item, response=response)
        loader.add_css('title', '.banner-heading h1::text')
        loader.add_css('lyrics', '.verse::text')
        yield loader.load_item()
