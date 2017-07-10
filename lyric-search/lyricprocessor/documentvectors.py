import collections
import gensim
import json
import nltk


SongVector = collections.namedtuple(
    'SongVector',
    ['artist', 'title', 'vector'])


class LyricCorpus:
    def __init__(self, filename):
        self.filename = filename
        self.dictionary = gensim.corpora.Dictionary()

    def __iter__(self):
        with open(self.filename) as song_file:
            for song_json in song_file:
                song = json.loads(song_json)
                lyric_tokens = nltk.word_tokenize(song['lyrics'])

                yield SongVector(
                    song['artist'],
                    song['title'],
                    self.dictionary.doc2bow(lyric_tokens, allow_update=True))


def lsi_vectors(corpus):
    tfidf = gensim.models.TfidfModel(song.vector for song in corpus)

    lsi = gensim.models.LsiModel(
        (tfidf[song.vector] for song in corpus),
        id2word=corpus.dictionary)

    return (SongVector(song.artist, song.title, lsi[tfidf[song.vector]])
            for song in corpus)
