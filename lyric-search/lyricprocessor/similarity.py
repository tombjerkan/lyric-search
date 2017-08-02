import gensim
import nltk

import database.tools
import database.models
from lyricprocessor import TfidfLsiModel

from configobj import ConfigObj
_config = ConfigObj('settings.cfg')


def _song_from_gensim_index(gensim_index):
    with database.tools.session_scope() as session:
        song_query = session.query(database.models.Song)

        # Gensim index is Numpy int so must be converted back to Python int
        song_query = song_query.filter(
            database.models.Song.id == int(gensim_index) + 1
        )

        song = song_query.scalar()
        return song


def similarity_to_song(song, num_best=10):
    """Returns the songs with the most similar lyrics to the given song.

    Returns a list of tuples (song, similarity) where the similarity is a
    float value between -1 and 1. The list is ordered from most similar to
    least. The number of songs in the list is specified by num_best.
    """
    index = gensim.similarities.Similarity.load(_config['INDEX_FILENAME'])

    # Add 1 as most similar list will include song itself which will then be
    # removed to give desired number of best
    index.num_best = num_best + 1

    # Subtract 1 from song ID as database starts mapping at 1, but gensim at 0
    similarities = index.similarity_by_id(song.id - 1)

    # Remove song itself (which will be most similar)
    del similarities[0]

    songs = [(_song_from_gensim_index(song_gensim_index), song_similarity)
             for (song_gensim_index, song_similarity) in similarities]

    return songs


def similarity_to_query(query_string, num_best=10):
    """Returns the songs with the most similar lyrics to a given query string.


    Returns a list of tuples (song index, similarity) where the similarity is
    a float value between -1 and 1. The list is ordered from most similar to
    least. The number of songs in the list is specified by num_best.

    The song IDs used refer to the ID stored in the database.
    """
    dictionary = gensim.corpora.Dictionary.load(_config['DICTIONARY_FILENAME'])
    model = TfidfLsiModel.load()

    query_tokens = nltk.word_tokenize(query_string)
    query_bow = dictionary.doc2bow(query_tokens)
    query_vector = model[query_bow]

    index = gensim.similarities.Similarity.load(_config['INDEX_FILENAME'])
    index.num_best = num_best
    similarities = index[query_vector]

    songs = [(_song_from_gensim_index(song_gensim_index), song_similarity)
             for (song_gensim_index, song_similarity) in similarities]

    return songs
