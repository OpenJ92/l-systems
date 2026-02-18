from __future__ import annotations
from typing import Self

class String(str):
    @classmethod
    def empty(cls) -> Self:
        return cls("")

    def combine(self, other: Self) -> Self:
        return type(self)(str(self) + str(other))

    def clone(self) -> Self:
        return self
