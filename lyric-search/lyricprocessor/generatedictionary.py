import gensim
import nltk
import sys

from lyricprocessor.lyriccorpus import database_lyrics


def main():
    dictionary_filename = sys.argv[1]

    dictionary = gensim.corpora.Dictionary(
        nltk.word_tokenize(lyrics)
        for lyrics in database_lyrics()
    )
    dictionary.save(dictionary_filename)


if __name__ == '__main__':
    main()
