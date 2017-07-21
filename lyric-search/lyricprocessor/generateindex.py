import gensim
import sys

from lyricprocessor import LyricCorpus
from lyricprocessor import TfidfLsiModel


def main():
    db_connection_string = sys.argv[1]
    dictionary_filename = sys.argv[2]
    tfidf_filename = sys.argv[3]
    lsi_filename = sys.argv[4]
    index_filename = sys.argv[5]

    dictionary = gensim.corpora.Dictionary.load(dictionary_filename)
    corpus = LyricCorpus(db_connection_string, dictionary)
    model = TfidfLsiModel.load(tfidf_filename, lsi_filename)
    index = gensim.similarities.Similarity(
        '/tmp/lyric-search.index',
        model[corpus],
        model.num_topics
    )
    index.save(index_filename)


if __name__ == '__main__':
    main()
