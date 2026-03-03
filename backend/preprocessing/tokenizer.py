import re


class Tokenizer:
    def tokenize(self, text: str) -> list[str]:
        return re.findall(r"[a-zA-Z0-9+#.]+", text)
