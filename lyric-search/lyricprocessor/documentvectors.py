import gensim
import json
import nltk


class LyricCorpus:
    def __init__(self, filename):
        self.filename = filename
        self.dictionary = gensim.corpora.Dictionary()

    def __iter__(self):
        with open(self.filename) as song_file:
            for song_json in song_file:
                song = json.loads(song_json)
                lyric_tokens = nltk.word_tokenize(song['lyrics'])
                yield self.dictionary.doc2bow(lyric_tokens, allow_update=True)


def lsi_vectors(lyric_corpus):
    tfidf_model = gensim.models.TfidfModel(lyric_corpus)
    tfidf_vectors = tfidf_model[lyric_corpus]

    lsi_model = gensim.models.LsiModel(tfidf_vectors,
                                       id2word=lyric_corpus.dictionary)
    lsi_vectors = lsi_model[tfidf_vectors]

    return lsi_vectors
