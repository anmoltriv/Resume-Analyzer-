from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from backend.preprocessing.boilerplate_remover import BoilerplateRemover
from backend.preprocessing.cleaner import TextCleaner
from backend.preprocessing.lemmatizer import Lemmatizer
from backend.preprocessing.tokenizer import Tokenizer


class PreprocessingPipeline:
    def __init__(
        self,
        cleaner: TextCleaner,
        tokenizer: Tokenizer,
        lemmatizer: Lemmatizer,
        boilerplate_remover: BoilerplateRemover,
    ):
        self.cleaner = cleaner
        self.tokenizer = tokenizer
        self.lemmatizer = lemmatizer
        self.boilerplate_remover = boilerplate_remover

    def process(self, text: str) -> str:
        text = self.boilerplate_remover.remove(text)
        text = self.cleaner.clean(text)
        tokens = self.tokenizer.tokenize(text)
        tokens = [token for token in tokens if token not in ENGLISH_STOP_WORDS]
        lemmas = self.lemmatizer.lemmatize(tokens)
        return " ".join(lemmas)
