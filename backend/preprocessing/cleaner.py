import re
import string


class TextCleaner:
    def clean(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"\s+", " ", text)
        return text.translate(str.maketrans("", "", string.punctuation)).strip()
