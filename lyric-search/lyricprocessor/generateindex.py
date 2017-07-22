import gensim
import sys

from lyricprocessor import LyricCorpus
from lyricprocessor import TfidfLsiModel


def main():
    index_filename = sys.argv[1]

    corpus = LyricCorpus()
    model = TfidfLsiModel.load()
    index = gensim.similarities.Similarity(
        '/tmp/lyric-search.index',
        model[corpus],
        model.num_topics
    )
    index.save(index_filename)


if __name__ == '__main__':
    main()
