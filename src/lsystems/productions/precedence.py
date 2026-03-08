from lsystems.protocols.production import Production


class Precedence(Production):
    """
    Ordered production dispatcher.

    Attempts each production in sequence and returns the first
    successful resolution.

    This enables layered production systems such as:

        ContextSensitive
        Stochastic
        Static

    where earlier productions have higher precedence.
    """

    def __init__(self, *productions: Production):
        self.productions = list(productions)

    def append(self, production: Production) -> None:
        """Append a production to the precedence chain."""
        self.productions.append(production)

    def resolve(self, symbol, scope):
        """
        Attempt to resolve productions in order.

        Returns the first successful rewrite or None if all fail.
        """
        for production in self.productions:
            result = production.resolve(symbol, scope)

            if result is not None:
                return result

        return None

    def __len__(self):
        return len(self.productions)
