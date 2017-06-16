import langdetect
from scrapy.exceptions import DropItem


class LyricsPipeline:
    def process_item(self, item, spider):
        if 'lyrics' in item:
            return item
        else:
            raise DropItem('Missing lyrics for {}'.format(item))


class LanguagePipeline:
    def process_item(self, item, spider):
        if langdetect.detect(item['lyrics']) == 'en':
            return item
        else:
            raise DropItem('Lyrics for {} are not in English'.format(item))
