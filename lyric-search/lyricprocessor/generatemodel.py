"""Generates the TF-IDF/LSI model for the song lyrics.

Generates the TfidfLsiModel that transforms lyric documents into vector
representations. The lyrics are taken from the database and saved to the two
model files, both specified in the config file.
"""

from lyricprocessor import LyricCorpus
from lyricprocessor import TfidfLsiModel


def main():
    corpus = LyricCorpus()
    model = TfidfLsiModel(corpus)
    model.save()


if __name__ == '__main__':
    main()
