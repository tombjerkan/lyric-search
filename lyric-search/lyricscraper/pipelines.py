import langdetect
from scrapy.exceptions import DropItem

import database.tools
import database.models


class LyricsPipeline:
    """Ensures songs have lyrics.

    Drops any SongItem that has not had lyrics assigned to it as songs without
    lyrics are not useful to the application.
    """

    def process_item(self, item, spider):
        """Returns item if it has lyrics, drops it if not."""
        if 'lyrics' in item:
            return item
        else:
            raise DropItem('Missing lyrics for {}'.format(item))


class LanguagePipeline:
    """Ensures song's lyrics are in English.

    Drops any SongItem whose lyrics are not in English as only these songs are
    wanted for the application.
    """

    def process_item(self, item, spider):
        """Returns item if its lyrics are in English, drops it if not.

        Language detection is not always correct so it is possible some songs
        with English lyrics are dropped and some songs with lyrics in other
        languages are not.
        """
        if langdetect.detect(item['lyrics']) == 'en':
            return item
        else:
            raise DropItem('Lyrics for {} are not in English'.format(item))


class DatabasePipeline:
    """Inserts each song's information into the database."""

    def process_item(self, item, spider):
        """Inserts a song into the database using fields from SongItem."""
        with database.tools.session_scope() as session:
            song = database.models.Song(
                artist = item['artist'],
                title = item['title'],
                lyrics = item['lyrics']
            )

            session.add(song)

        return item
