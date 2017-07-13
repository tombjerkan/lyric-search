import collections
import gensim
import json
import nltk


SongVector = collections.namedtuple(
    'SongVector',
    ['artist', 'title', 'vector']
)


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
                    song['artist'] if 'artist' in song else None,
                    song['title'] if 'title' in song else None,
                    self.dictionary.doc2bow(lyric_tokens, allow_update=True)
                )


def document_vectors(corpus):
    tfidf = gensim.models.TfidfModel(song.vector for song in corpus)

    lsi = gensim.models.LsiModel(
        (tfidf[song.vector] for song in corpus),
        id2word=corpus.dictionary
    )

    for song in corpus:
        lsi_vector = lsi[tfidf[song.vector]]
        lsi_vector = [topic_value for _, topic_value in lsi_vector]
        lsi_vector = tuple(lsi_vector)
        yield SongVector(song.artist, song.title, lsi_vector)


def save_vectors(songs, file):
    for song in songs:
        song_json = json.dumps({
            'artist': song.artist,
            'title': song.title,
            'vector': song.vector
        })

        file.write(song_json + '\n')
