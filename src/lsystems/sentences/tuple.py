from __future__ import annotations
from typing import Self

class Tuple(tuple):
    @classmethod
    def empty(cls) -> Self:
        return cls(())

    def combine(self, other: Self) -> Self:
        return type(self)(tuple(self) + tuple(other))

    def clone(self) -> Self:
        return self
