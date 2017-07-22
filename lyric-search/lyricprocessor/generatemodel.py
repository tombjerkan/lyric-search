import gensim
import sys

from lyricprocessor import LyricCorpus
from lyricprocessor import TfidfLsiModel


def main():
    dictionary_filename = sys.argv[1]
    tfidf_filename = sys.argv[2]
    lsi_filename = sys.argv[3]

    dictionary = gensim.corpora.Dictionary.load(dictionary_filename)
    corpus = LyricCorpus(dictionary)
    model = TfidfLsiModel(corpus)
    model.save(tfidf_filename, lsi_filename)


if __name__ == '__main__':
    main()
