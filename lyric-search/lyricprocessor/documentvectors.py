import gensim
import json
import nltk


def create_dictionary(song_file):
    dictionary = gensim.corpora.Dictionary()

    for song_json in song_file:
        song = json.loads(song_json)
        lyrics = song['lyrics']
        lyric_tokens = nltk.word_tokenize(lyrics)
        dictionary.add_documents([lyric_tokens])

    return dictionary


def create_document_vectors(dictionary, song_file):
    document_vectors = []

    for song_json in song_file:
        song = json.loads(song_json)
        lyrics = song['lyrics']
        lyric_tokens = nltk.word_tokenize(lyrics)
        document_vectors.append(dictionary.doc2bow(lyric_tokens))

    return document_vectors
