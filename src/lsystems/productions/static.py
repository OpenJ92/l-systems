from src.lsystems.protocols.sentence import Sentence
from src.lsystems.protocols.production import Production
from src.lsystems.generate import ScopeBundle
from collections.abc import Hashable

class Static(Production):
    def __init__(self, sentence: Sentence):
        self.sentence = sentence.clone()

    def __call__(self, symbol: Hashable, scope: ScopeBundle):
        return self.sentence
