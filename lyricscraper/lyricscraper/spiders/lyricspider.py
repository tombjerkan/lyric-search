import scrapy
import string

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
        next_page_link = response.css('.next::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.artist_parse)
