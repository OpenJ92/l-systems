from typing import Self

class Tuple(tuple):
    @classmethod
    def empty(cls) -> Self:
        return cls(())
    @classmethod
    def lift(cls, symbol):
        return cls((symbol,))

    def combine(self, other: Self) -> Self:
        return type(self)(self + other)

    def clone(self) -> Self:
        return self
