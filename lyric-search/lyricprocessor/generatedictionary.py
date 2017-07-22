import gensim
import nltk
import sys

from lyricprocessor.lyriccorpus import database_lyrics

from configobj import ConfigObj
config = ConfigObj('settings.cfg')


def main():
    dictionary = gensim.corpora.Dictionary(
        nltk.word_tokenize(lyrics)
        for lyrics in database_lyrics()
    )
    dictionary.save(config['DICTIONARY_FILENAME'])


if __name__ == '__main__':
    main()
