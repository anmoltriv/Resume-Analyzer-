from nltk.stem import PorterStemmer


class Lemmatizer:
    def __init__(self):
        self._stemmer = PorterStemmer()

    def lemmatize(self, tokens: list[str]) -> list[str]:
        return [self._stemmer.stem(token) for token in tokens]
