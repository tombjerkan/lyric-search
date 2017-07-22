import gensim
import sys

from lyricprocessor import LyricCorpus
from lyricprocessor import TfidfLsiModel


def main():
    tfidf_filename = sys.argv[1]
    lsi_filename = sys.argv[2]

    corpus = LyricCorpus()
    model = TfidfLsiModel(corpus)
    model.save(tfidf_filename, lsi_filename)


if __name__ == '__main__':
    main()
