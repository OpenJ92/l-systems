from __future__ import annotations

from lsystems.protocols.sentence import Sentence
from lsystems.protocols.production import Production
from collections.abc import Hashable

from dataclasses import dataclass
from bisect import bisect_right
from random import randrange
from typing import Generic, TypeVar, Optional

class Stochastic(Production):
    def __init__(self):
        self.total = 0
        self._cutoffs : List[int] = []
        self._sentences : List[Sentence] = []

    def add(self, frequency: int, sentence: Sentence) -> None:
        """
        Add `frequency` mass for `sentence`.

        Constraints:
          - frequency must be > 0 (0 is a no-op; negatives are invalid)
        """
        if frequency <= 0:
            raise ValueError(f"frequency must be positive, got {frequency}")

        self.total += frequency
        self._cutoffs.append(self.total)
        self._sentences.append(sentence)

    def sample(self, rng) -> Sentence:
        """
        Sample one Sentence proportional to its frequency.
        """
        if self.total <= 0:
            raise LookupError("Cannot sample from an empty Stochastic distribution")

        r = rng.randrange(self.total)          # integer in [0, total)
        i = bisect_right(self._cutoffs, r) # locate bucket
        return self._sentences[i]

    def __call__(self, symbol: Symbol, scope: ScopeBundle) -> Sentence:
        """
        Production interface: ignore symbol/scope by default and just sample a sentence.
        """
        return self.sample(scope.run.random)

    def __len__(self) -> int:
        return len(self._sentences)

    def clear(self) -> None:
        self.total = 0
        self._cutoffs.clear()
        self._sentences.clear()
