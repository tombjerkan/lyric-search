import gensim
import nltk
import sqlalchemy

import database.tools
import database.models

from configobj import ConfigObj
_config = ConfigObj('settings.cfg')


def database_lyrics():
    """Iterates over the lyrics for each song in the database."""
    with database.tools.session_scope() as session:
        song_query = session.query(database.models.Song)
        song_query = song_query.order_by(database.models.Song.id)

        for song in song_query:
            yield song.lyrics


class LyricCorpus:
    """A corpus that yields the bag-of-words vector for each song's lyrics."""

    def __init__(self):
        """Initialises the corpus dictionary for use when yielding vectors."""
        self.dictionary = gensim.corpora.Dictionary.load(
            _config['DICTIONARY_FILENAME']
        )

    def __iter__(self):
        """Yields the bag-of-words vector for each song's lyrics."""
        for lyrics in database_lyrics():
            lyric_tokens = nltk.word_tokenize(lyrics)
            yield self.dictionary.doc2bow(lyric_tokens)

    def __len__(self):
        """Returns the number of songs in the corpus."""
        with database.tools.session_scope() as session:
            count_query = session.query(
                sqlalchemy.func.count(database.models.Song.id)
            )

            return count_query.scalar()
