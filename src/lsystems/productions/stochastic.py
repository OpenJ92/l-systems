from __future__ import annotations

from lsystems.protocols.sentence import Sentence
from lsystems.protocols.production import Production
from collections.abc import Hashable

from dataclasses import dataclass
from bisect import bisect_right
from random import randrange
from typing import Generic, TypeVar, Optional

class Stochastic(Production):
    """
    Probabilistic production.

    Sentences are selected according to weighted frequencies.
    """

    def __init__(self):
        self.total = 0
        self._cutoffs = []
        self._sentences = []

    def add(self, frequency, sentence):
        """
        Add a stochastic rule with the given frequency weight.
        """

        if frequency <= 0:
            raise ValueError("frequency must be positive")

        self.total += frequency
        self._cutoffs.append(self.total)
        self._sentences.append(sentence)

    def sample(self, rng):
        """
        Sample a sentence from the distribution.
        """

        if self.total <= 0:
            raise LookupError("Cannot sample from an empty distribution")

        r = rng.randrange(self.total)
        i = bisect_right(self._cutoffs, r)

        return self._sentences[i]

    def resolve(self, symbol, scope):
        """
        Resolve by sampling from the run RNG.
        """
        return self.sample(scope.run.rng)

    def clear(self):
        """Remove all stochastic rules."""
        self.total = 0
        self._cutoffs.clear()
        self._sentences.clear()

    def __len__(self):
        return len(self._sentences)
