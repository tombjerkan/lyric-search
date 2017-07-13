#!/usr/bin/env python3

import collections
import gensim
import json
import nltk
import sys


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


def main():
    lyrics_input_filename = sys.argv[1]
    vectors_output_filename = sys.argv[2]

    corpus = LyricCorpus(lyrics_input_filename)
    vectors = document_vectors(corpus)

    with open(vectors_output_filename, 'w') as output_file:
        save_vectors(vectors, output_file)


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


if __name__ == '__main__':
    main()
