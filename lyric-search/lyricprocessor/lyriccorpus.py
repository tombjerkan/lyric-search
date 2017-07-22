import gensim
import nltk
import sqlalchemy

import database.tools
import database.models

from configobj import ConfigObj
config = ConfigObj('settings.cfg')


def database_lyrics():
    with database.tools.session_scope() as session:
        song_query = session.query(database.models.Song)
        song_query = song_query.order_by(database.models.Song.id)

        for song in song_query:
            yield song.lyrics


class LyricCorpus:
    def __init__(self):
        self.dictionary = gensim.corpora.Dictionary.load(
            config['DICTIONARY_FILENAME']
        )

    def __iter__(self):
        for lyrics in database_lyrics():
            lyric_tokens = nltk.word_tokenize(lyrics)
            yield self.dictionary.doc2bow(lyric_tokens)

    def __len__(self):
        with database.tools.session_scope() as session:
            count_query = session.query(
                sqlalchemy.func.count(database.models.Song.id)
            )

            return count_query.scalar()
