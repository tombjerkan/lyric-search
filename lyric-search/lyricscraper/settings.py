# -*- coding: utf-8 -*-

# Scrapy settings for lyricscraper project

BOT_NAME = 'lyricscraper'

SPIDER_MODULES = ['lyricscraper.spiders']
NEWSPIDER_MODULE = 'lyricscraper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'lyricscraper.pipelines.LyricsPipeline': 0,
    'lyricscraper.pipelines.LanguagePipeline': 1,
    'lyricscraper.pipelines.DatabasePipeline': 2
}
