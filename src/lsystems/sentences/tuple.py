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

    def left_of(self, index: int, width: int):
        """
        Return the left context of the given width.

        Returns None if the requested context would extend
        beyond the sentence boundary.
        """

        if width == 0:
            return type(self).empty()

        if index < width:
            return None

        return type(self)(self[index - width:index])

    def right_of(self, index: int, width: int):
        """
        Return the right context of the given width.

        Returns None if the requested context would extend
        beyond the sentence boundary.
        """

        if width == 0:
            return type(self).empty()

        start = index + 1
        stop = start + width

        if stop > len(self):
            return None

        return type(self)(self[start:stop])
