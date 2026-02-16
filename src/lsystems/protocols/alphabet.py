from typing import Protocol

class Alphabet(Protocol):
    def contains(self, letter):
        raise NotImplementedError

    def boundary(self):
        raise NotImplementedError
