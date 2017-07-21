import sys

from lyricprocessor.documentvectors import LyricCorpus
from lyricprocessor.documentvectors import TfidfLsiModel


def main():
    db_connection_string = sys.argv[1]
    tfidf_filename = sys.argv[2]
    lsi_filename = sys.argv[3]

    corpus = LyricCorpus(db_connection_string)
    model = TfidfLsiModel(corpus)
    model.save(tfidf_filename, lsi_filename)


if __name__ == '__main__':
    main()
