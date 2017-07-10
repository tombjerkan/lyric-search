import gensim
import json
import nltk


class LyricCorpus:
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename) as song_file:
            for song_json in song_file:
                song = json.loads(song_json)
                yield nltk.word_tokenize(song['lyrics'])


def create_dictionary(lyric_corpus):
    return gensim.corpora.Dictionary(lyric_corpus)


def create_document_vectors(dictionary, lyric_corpus):
    return [dictionary.doc2bow(lyric_tokens) for lyric_tokens in lyric_corpus]
