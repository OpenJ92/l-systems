from collections import OrderedDict

from lsystems.protocols.production import Production
from lsystems.productions.precedence import Precedence


class ContextSensitive(Production):
    """
    Fixed-width context sensitive production.

    Rules match based on exact left and right context sizes.

    Example
    -------
        empty > A < B

    would be represented with:

        ContextSensitive(0, 1)

    and rule:

        ("", "B") -> replacement
    """

    def __init__(self, left_width: int, right_width: int):
        if left_width < 0:
            raise ValueError("left_width must be non-negative")

        if right_width < 0:
            raise ValueError("right_width must be non-negative")

        self.left_width = left_width
        self.right_width = right_width
        self._rules = {}

    def add(self, left, right, sentence):
        """
        Add a context-sensitive rule.

        Parameters
        ----------
        left
            Sentence representing the left context

        right
            Sentence representing the right context

        sentence
            Replacement sentence
        """

        if len(left) != self.left_width:
            raise ValueError("Left context width mismatch")

        if len(right) != self.right_width:
            raise ValueError("Right context width mismatch")

        self._rules[(left, right)] = sentence

    def resolve(self, symbol, scope):
        """
        Attempt to match the surrounding context.

        If a rule matches the left and right context,
        its replacement sentence is returned.
        """

        sentence = scope.generation.sentence
        index = scope.position.index

        left = sentence.left_of(index, self.left_width)

        if left is None:
            return None

        right = sentence.right_of(index, self.right_width)

        if right is None:
            return None

        return self._rules.get((left, right))

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

    Wider contexts are automatically evaluated first.
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
            Iterable of (left, right, replacement)

        Rules are grouped by context width automatically.
        """

        groups = OrderedDict()

        for left, right, replacement in rules:
            key = (len(left), len(right))

            if key not in groups:
                groups[key] = ContextSensitive(*key)

            groups[key].add(left, right, replacement)

        return cls(*groups.values(), fallback=fallback, auto_order=auto_order)
