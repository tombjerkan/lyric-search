import gensim

from lyricprocessor import LyricCorpus
from lyricprocessor import TfidfLsiModel

from configobj import ConfigObj
config = ConfigObj('settings.cfg')


def main():
    corpus = LyricCorpus()
    model = TfidfLsiModel.load()
    index = gensim.similarities.Similarity(
        '/tmp/lyric-search.index',
        model[corpus],
        model.num_topics
    )
    index.save(config['INDEX_FILENAME'])


if __name__ == '__main__':
    main()
