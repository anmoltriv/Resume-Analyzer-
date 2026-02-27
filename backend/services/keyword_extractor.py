from __future__ import annotations

from collections import Counter
from typing import List


def extract_keywords(tokens: List[str], min_frequency: int = 1) -> List[str]:
    """Extract unique keywords ordered by frequency then first appearance."""
    if not tokens:
        return []

    frequency_counter: Counter[str] = Counter(tokens)
    first_position: dict[str, int] = {}
    for index, token in enumerate(tokens):
        if token not in first_position:
            first_position[token] = index

    sorted_keywords: List[str] = sorted(
        [token for token, count in frequency_counter.items() if count >= min_frequency],
        key=lambda token: (-frequency_counter[token], first_position[token]),
    )
    return sorted_keywords
