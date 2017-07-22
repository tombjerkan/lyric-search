import gensim
import sys

from lyricprocessor import LyricCorpus
from lyricprocessor import TfidfLsiModel


def main():
    tfidf_filename = sys.argv[1]
    lsi_filename = sys.argv[2]
    index_filename = sys.argv[3]

    corpus = LyricCorpus()
    model = TfidfLsiModel.load(tfidf_filename, lsi_filename)
    index = gensim.similarities.Similarity(
        '/tmp/lyric-search.index',
        model[corpus],
        model.num_topics
    )
    index.save(index_filename)


if __name__ == '__main__':
    main()
