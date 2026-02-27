from __future__ import annotations

import re
from typing import List, Set

STOPWORDS: Set[str] = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "if",
    "in",
    "into",
    "is",
    "it",
    "no",
    "not",
    "of",
    "on",
    "or",
    "such",
    "that",
    "the",
    "their",
    "then",
    "there",
    "these",
    "they",
    "this",
    "to",
    "was",
    "will",
    "with",
    "you",
    "your",
    "from",
    "we",
    "our",
    "i",
    "me",
    "my",
    "he",
    "she",
    "his",
    "her",
    "them",
    "those",
}


def preprocess_text(text: str) -> List[str]:
    """Lowercase text, remove punctuation, stopwords, and tokenize."""
    lowered: str = text.lower()
    cleaned: str = re.sub(r"[^a-z0-9\s]", " ", lowered)
    tokens: List[str] = cleaned.split()
    filtered_tokens: List[str] = [token for token in tokens if token not in STOPWORDS]
    return filtered_tokens
