from lsystems.protocols.production import Production


class Generation(Production):
    """
    Generation-indexed production.

    Selects a production based on scope.generation.generation.
    """

    def __init__(self, fallback: Production | None = None):
        self._rules = {}
        self.fallback = fallback

    def add(self, generation: int, production: Production):
        self._rules[generation] = production

    def resolve(self, symbol, scope):
        generation = scope.generation.generation
        production = self._rules.get(generation)

        if production is not None:
            return production.resolve(symbol, scope)

        if self.fallback is not None:
            return self.fallback.resolve(symbol, scope)

        return None
