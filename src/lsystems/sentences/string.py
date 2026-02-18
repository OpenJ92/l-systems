from __future__ import annotations
from typing import Self

class String(str):
    @classmethod
    def empty(cls) -> Self:
        return cls("")
    @classmethod
    def lift(cls, symbol):
        return cls(f"{symbol}")

    def combine(self, other: Self) -> Self:
        return type(self)(self + other)

    def clone(self) -> Self:
        return self
