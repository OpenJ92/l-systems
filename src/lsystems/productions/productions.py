class Productions():
    def __init__(self):
        self.productions = defaultdict(lambda x: x)

    def add(self, symbol, rule):
        self.productions[symbol] = rule

    def get(self, symbol):
        return self.productions[symbol]
