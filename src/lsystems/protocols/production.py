from typing import Protocol

class Production(Protocol):
    def __call__(self, symbol, context):
        ...
