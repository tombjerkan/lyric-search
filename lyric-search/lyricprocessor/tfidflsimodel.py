import gensim


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

    def save(self, tfidf_filename, lsi_filename):
        self.tfidf.save(tfidf_filename)
        self.lsi.save(lsi_filename)

    @classmethod
    def load(cls, tfidf_filename, lsi_filename):
        model = TfidfLsiModel()
        model.tfidf = gensim.models.TfidfModel.load(tfidf_filename)
        model.lsi = gensim.models.LsiModel.load(lsi_filename)
        return model
