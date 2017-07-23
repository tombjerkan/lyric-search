import gensim

from lyricprocessor import LyricCorpus
from lyricprocessor import TfidfLsiModel

from configobj import ConfigObj
_config = ConfigObj('settings.cfg')


def main():
    corpus = LyricCorpus()
    model = TfidfLsiModel.load()
    index = gensim.similarities.Similarity(
        '/tmp/lyric-search.index',
        model[corpus],
        model.num_topics
    )
    index.save(_config['INDEX_FILENAME'])


if __name__ == '__main__':
    main()
