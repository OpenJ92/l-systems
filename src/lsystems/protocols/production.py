from typing import Protocol, runtime_checkable
from lsystems.protocols.sentence import Sentence

from typing import Protocol, runtime_checkable

@runtime_checkable
class Production(Protocol):
    """
    Base protocol for all L-system productions.

    The production system operates in two layers:

    resolve(symbol, scope)
        Attempt to produce a rewrite result.

        Returns:
            Sentence  -> this production applies
            None      -> this production does not apply

    __call__(symbol, scope)
        Total production interface used by the generator.

        If resolve() returns None, the symbol rewrites to itself
        (identity production).
    """

    def resolve(self, symbol, scope) -> Sentence | None:
        """
        Attempt to resolve a rewrite for the given symbol and scope.

        Returns
        -------
        Sentence
            The replacement sentence if this production applies.

        None
            If this production does not apply.
        """
        ...

    def __call__(self, symbol, scope) -> Sentence:
        """
        Execute the production.

        This method guarantees a valid rewrite by falling back
        to the identity production when resolve() fails.
        """
        result = self.resolve(symbol, scope)

        if result is not None:
            return result

        return type(scope.generation.sentence).lift(symbol)
