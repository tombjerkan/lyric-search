import scrapy
import string

from lyricscraper.items import SongItemLoader

class LyricSpider(scrapy.Spider):
    name = 'lyricspider'

    # Starts at the initial page for artists grouped alphabetically
    start_urls = ['http://www.metrolyrics.com/artists-{}.html'.format(letter)
                  for letter in string.ascii_lowercase]

    def parse(self, response):
        artist_selector = '//table[@class="songs-table"]/tbody/tr/td/a/@href'
        for artist_link in response.xpath(artist_selector):
            yield response.follow(artist_link, callback=self.artist_parse)

        next_page_link = response.css('.next::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

    def artist_parse(self, response):
        artist_name = response.css('.artist-header h1 ::text').extract_first()

        song_selector = '#popular .songs-table a::attr(href)'
        song_links = response.css(song_selector).extract()
        for song_link in song_links:
            yield response.follow(song_link, callback=self.song_parse,
                                  meta={'artist': artist_name})

        next_page_link = response.css('.next::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.artist_parse)

    def song_parse(self, response):
        song_header_selector = '.lyrics header h1::text'

        loader = SongItemLoader(response=response)
        loader.add_value('artist', response.meta['artist'])
        loader.add_css('title', song_header_selector)
        yield loader.load_item()