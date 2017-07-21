#!/usr/bin/env python3

import gensim
import nltk
import sqlalchemy
import sys

import database.tools
import database.models


class LyricCorpus:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.dictionary = gensim.corpora.Dictionary()

    def __iter__(self):
        with database.tools.session_scope(self.connection_string) as session:
            song_query = session.query(database.models.Song)
            song_query = song_query.order_by(database.models.Song.id)

            for song in song_query:
                lyric_tokens = nltk.word_tokenize(song.lyrics)
                yield self.dictionary.doc2bow(lyric_tokens, allow_update=True)

    def __len__(self):
        with database.tools.session_scope(self.connection_string) as session:
            count_query = session.query(
                sqlalchemy.func.count(database.models.Song.id)
            )

            return count_query.scalar()


class TfidfLsiModel:
    def __init__(self, corpus):
        self.tfidf = gensim.models.TfidfModel(corpus)
        self.lsi = gensim.models.LsiModel(corpus, id2word=corpus.dictionary)

    def __getitem__(self, item):
        return self.lsi[self.tfidf[item]]

    @property
    def num_topics(self):
        return self.lsi.num_topics


def main():
    db_connection_string = sys.argv[1]
    index_filename = sys.argv[2]

    corpus = LyricCorpus(db_connection_string)
    model = TfidfLsiModel(corpus)
    vectors = model[corpus]
    save_vectors(vectors, db_connection_string)

    index = gensim.similarities.Similarity(
        '/tmp/lyric-search.index',
        vectors,
        model.num_topics
    )
    index.save(index_filename)


def save_vectors(vectors, connection_string):
    with database.tools.session_scope(connection_string) as session:
        for song_index, vector in enumerate(vectors, 1):
            for feature in vector:
                feature_index, feature_value = feature

                feature = database.models.VectorFeature(
                    song_id=song_index,
                    index=int(feature_index),
                    value=float(feature_value)
                )

                session.add(feature)


if __name__ == '__main__':
    main()
