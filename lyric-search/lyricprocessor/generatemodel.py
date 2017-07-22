from lyricprocessor import LyricCorpus
from lyricprocessor import TfidfLsiModel


def main():
    corpus = LyricCorpus()
    model = TfidfLsiModel(corpus)
    model.save()


if __name__ == '__main__':
    main()
