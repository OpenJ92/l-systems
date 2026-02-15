from typing import Protocol

class Sentence(Protocol):
    def combine(self, other):
        raise NotImplementedError

    def mempty(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, index: int):
        raise NotImplementedError
