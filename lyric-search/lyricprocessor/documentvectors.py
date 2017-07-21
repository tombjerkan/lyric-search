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
    def __init__(self, corpus=None):
        if corpus is not None:
            self.tfidf = gensim.models.TfidfModel(corpus)
            self.lsi = gensim.models.LsiModel(
                corpus,
                id2word=corpus.dictionary
            )

    def __getitem__(self, item):
        return self.lsi[self.tfidf[item]]

    @property
    def num_topics(self):
        return self.lsi.num_topics

    def save(self, tfidf_filename, lsi_filename):
        self.tfidf.save(tfidf_filename)
        self.lsi.save(lsi_filename)

    @classmethod
    def load(cls, tfidf_filename, lsi_filename):
        model = TfidfLsiModel()
        model.tfidf = gensim.models.TfidfModel.load(tfidf_filename)
        model.lsi = gensim.models.LsiModel.load(lsi_filename)
        return model


def main():
    db_connection_string = sys.argv[1]
    tfidf_filename = sys.argv[2]
    lsi_filename = sys.argv[3]
    index_filename = sys.argv[4]

    corpus = LyricCorpus(db_connection_string)

    model = TfidfLsiModel.load(tfidf_filename, lsi_filename)

    vectors = model[corpus]

    index = gensim.similarities.Similarity(
        '/tmp/lyric-search.index',
        vectors,
        model.num_topics
    )
    index.save(index_filename)


if __name__ == '__main__':
    main()
