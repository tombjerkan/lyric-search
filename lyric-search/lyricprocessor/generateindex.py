import gensim
import sys

from lyricprocessor.documentvectors import LyricCorpus
from lyricprocessor.documentvectors import TfidfLsiModel


def main():
    db_connection_string = sys.argv[1]
    tfidf_filename = sys.argv[2]
    lsi_filename = sys.argv[3]
    index_filename = sys.argv[4]

    corpus = LyricCorpus(db_connection_string)
    model = TfidfLsiModel.load(tfidf_filename, lsi_filename)
    index = gensim.similarities.Similarity(
        '/tmp/lyric-search.index',
        model[corpus],
        model.num_topics
    )
    index.save(index_filename)


if __name__ == '__main__':
    main()
