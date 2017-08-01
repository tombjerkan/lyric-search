"""Generates a dictionary of words from song lyrics.

Generates a Gensim Dictionary object that maps word strings to ID values to be
used throughout the lyric processing. The lyrics are taken from the database
and the resulting dictionary is saved to the dictionary file, both specified
in the config file.
"""

import gensim
import nltk

from lyricprocessor.lyriccorpus import database_lyrics

from configobj import ConfigObj
_config = ConfigObj('settings.cfg')


def main():
    dictionary = gensim.corpora.Dictionary(
        nltk.word_tokenize(lyrics)
        for lyrics in database_lyrics()
    )
    dictionary.save(_config['DICTIONARY_FILENAME'])


if __name__ == '__main__':
    main()
