import gensim

from configobj import ConfigObj
config = ConfigObj('settings.cfg')


class TfidfLsiModel:
    def __init__(self, corpus=None):
        if corpus is not None:
            self.tfidf = gensim.models.TfidfModel(corpus)
            self.lsi = gensim.models.LsiModel(
                corpus,
                id2word=corpus.dictionary
            )

    def __getitem__(self, item):
        return self.lsi[self.tfidf[item]]

    @property
    def num_topics(self):
        return self.lsi.num_topics

    def save(self):
        self.tfidf.save(config['TFIDF_MODEL_FILENAME'])
        self.lsi.save(config['LSI_MODEL_FILENAME'])

    @classmethod
    def load(cls):
        model = TfidfLsiModel()
        model.tfidf = gensim.models.TfidfModel.load(
            config['TFIDF_MODEL_FILENAME']
        )
        model.lsi = gensim.models.LsiModel.load(
            config['LSI_MODEL_FILENAME']
        )
        return model
