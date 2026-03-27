from lsystems.protocols.production import Production

class Static(Production):
    """
    Deterministic production.

    Always replaces the symbol with the same sentence.
    """

    def __init__(self, sentence):
        self.sentence = sentence

    def resolve(self, symbol, scope):
        return self.sentence
