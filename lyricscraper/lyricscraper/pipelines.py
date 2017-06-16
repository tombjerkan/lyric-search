import langdetect
from scrapy.exceptions import DropItem


class LyricsPipeline:
    def process_item(self, item, spider):
        if 'lyrics' not in item:
            raise DropItem('Missing lyrics for {}'.format(item))
        else:
            return item


class LanguagePipeline:
    def process_item(self, item, spider):
        if langdetect.detect(item['lyrics']) != 'en':
            raise DropItem('Lyrics for {} are not in English'.format(item))
        else:
            return item
