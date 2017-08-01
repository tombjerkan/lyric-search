"""Generates the similarity index for the song lyrics.

Generates a Gensim similarity index to be used when querying lyric similarity.
The lyrics are taken from the database, the TF-IDF/LSI model is loaded from
previously generated files and the resulting index is saved to the index file,
all specified in the config file.
"""

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
