from collections import OrderedDict

from lsystems.protocols.production import Production
from lsystems.productions.precedence import Precedence


class ContextSensitive(Production):
    """
    Fixed-width context sensitive production.
    """

    def __init__(self, left_width: int, right_width: int, fallback: Production | None = None):
        if left_width < 0:
            raise ValueError("left_width must be non-negative")

        if right_width < 0:
            raise ValueError("right_width must be non-negative")

        self.left_width = left_width
        self.right_width = right_width
        self._rules = {}
        self.fallback = fallback

    def add(self, left, right, production: Production):
        """
        Add a context-sensitive rule.
        """

        if len(left) != self.left_width:
            raise ValueError("Left context width mismatch")

        if len(right) != self.right_width:
            raise ValueError("Right context width mismatch")

        self._rules[(left, right)] = production

    def resolve(self, symbol, scope):
        """
        Attempt to match the surrounding context.

        If a rule matches the left and right context,
        its production is resolved.
        """

        sentence = scope.generation.sentence
        index = scope.position.index

        left = sentence.left_of(index, self.left_width)
        if left is None:
            if self.fallback is not None:
                return self.fallback.resolve(symbol, scope)
            return None

        right = sentence.right_of(index, self.right_width)
        if right is None:
            if self.fallback is not None:
                return self.fallback.resolve(symbol, scope)
            return None

        production = self._rules.get((left, right))
        if production is not None:
            return production.resolve(symbol, scope)

        if self.fallback is not None:
            return self.fallback.resolve(symbol, scope)

        return None

    def clear(self):
        """Remove all rules."""
        self._rules.clear()

    def __len__(self):
        return len(self._rules)


class VariationalContextSensitive(Precedence):
    """
    Variable-width context sensitive production.

    This class wraps multiple fixed-width ContextSensitive
    productions inside a precedence dispatcher.
    """

    def __init__(self, *contexts: ContextSensitive, fallback=None, auto_order=True):
        ordered = list(contexts)

        if auto_order:
            ordered.sort(
                key=lambda c: (
                    c.left_width + c.right_width,
                    c.left_width,
                    c.right_width,
                ),
                reverse=True,
            )

        if fallback is not None:
            ordered.append(fallback)

        super().__init__(*ordered)

    @classmethod
    def from_rules(cls, rules, fallback=None, auto_order=True):
        """
        Build a variational context system from raw rules.

        Parameters
        ----------
        rules
            Iterable of (left, right, production)
        """

        groups = OrderedDict()

        for left, right, production in rules:
            key = (len(left), len(right))

            if key not in groups:
                groups[key] = ContextSensitive(*key)

            groups[key].add(left, right, production)

        return cls(*groups.values(), fallback=fallback, auto_order=auto_order)
