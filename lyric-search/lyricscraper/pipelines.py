import langdetect
from scrapy.exceptions import DropItem

import database.tools
import database.models


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


class DatabasePipeline:
    def process_item(self, item, spider):
        with database.tools.session_scope() as session:
            song = database.models.Song(
                artist = item['artist'],
                title = item['title'],
                lyrics = item['lyrics']
            )

            session.add(song)

        return item
