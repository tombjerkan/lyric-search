import gensim
import nltk
import sys

from lyricprocessor.lyriccorpus import database_lyrics


def main():
    db_connection_string = sys.argv[1]
    dictionary_filename = sys.argv[2]

    dictionary = gensim.corpora.Dictionary(
        nltk.word_tokenize(lyrics)
        for lyrics in database_lyrics(db_connection_string)
    )
    dictionary.save(dictionary_filename)


if __name__ == '__main__':
    main()
