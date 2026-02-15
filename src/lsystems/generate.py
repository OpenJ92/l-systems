class Generate():
    def __init__(self, lsystem: LSystem, depth: int, context: Context):
        self.lsystem = lsystem
        self.depth = depth
        self.context = context

    def run_generation(self, generation: int):
        alphabet = self.lsystem.alphabet
        productions = self.lsystem.productions
        sentence = self.lsystem.sentence

        rewrites = []
        for index, symbol in enumerate(sentence):
            production = productions.get(symbol)
            self.context.evolve(sentence, index, generation)
            rewrite = production(symbol, self.context)
            rewrites.append(rewrite)

        sentence = sentence.empty()
        for rewrite in rewrites:
            sentence = sentence.combine(rewrite)

        return sentence

    def run(self):
        sentence = self.lsystem.sentence
        for _ in range(self.depth):
            sentence = self.run_generation()
            

def Run(generate: Generate):
    return generate.run()
