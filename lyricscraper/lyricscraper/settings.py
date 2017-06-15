# -*- coding: utf-8 -*-

# Scrapy settings for lyricscraper project

BOT_NAME = 'lyricscraper'

SPIDER_MODULES = ['lyricscraper.spiders']
NEWSPIDER_MODULE = 'lyricscraper.spiders'

ROBOTSTXT_OBEY = True

FEED_URI = 'songs.json'
FEED_FORMAT = 'jsonlines'
