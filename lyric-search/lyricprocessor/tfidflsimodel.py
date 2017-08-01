import gensim

from configobj import ConfigObj
_config = ConfigObj('settings.cfg')


class TfidfLsiModel:
    """A model for the combined application of a TF-IDF and an LSI model."""

    def __init__(self, corpus=None):
        """Initialises the model from a corpus if given.

        If corpus is not None, then the lyrics from the corpus are used to
        initialise the TFIDF model which is then used to initialise the LSI
        model.

        If corpus is None then the model remains uninitialised and must have
        its models (tfidf and lsi) set manually.
        """
        if corpus is not None:
            self.tfidf = gensim.models.TfidfModel(corpus)
            self.lsi = gensim.models.LsiModel(
                corpus,
                id2word=corpus.dictionary
            )

    def __getitem__(self, item):
        """Returns the result of applying the model to the given item.

        The item can be either a corpus or a single document.
        """
        return self.lsi[self.tfidf[item]]

    @property
    def num_topics(self):
        return self.lsi.num_topics

    def save(self):
        """Saves the internal TF-IDF and LSI models.

        The models are saved at the locations specified in the config file.
        """
        self.tfidf.save(_config['TFIDF_MODEL_FILENAME'])
        self.lsi.save(_config['LSI_MODEL_FILENAME'])

    @classmethod
    def load(cls):
        """Returns TfidfLsiModel with internal models loaded from files.

        The locations of the models are specified in the config file.
        """
        model = TfidfLsiModel()
        model.tfidf = gensim.models.TfidfModel.load(
            _config['TFIDF_MODEL_FILENAME']
        )
        model.lsi = gensim.models.LsiModel.load(
            _config['LSI_MODEL_FILENAME']
        )
        return model
