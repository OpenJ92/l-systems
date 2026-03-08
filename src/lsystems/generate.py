import random

class RunScope():
    def __init__(self, name, lsystem, seed):
        self.name = name
        self.lsystem = lsystem

        if seed is None:
            seed = random.randrange(2**64)

        self.seed = seed
        self.rng = random.Random(seed)

class GenerationScope():
    def __init__(self, depth, generation, sentence):
        self.depth = depth
        self.generation = generation
        self.sentence = sentence

class PositionScope():
    def __init__(self, index, symbol):
        self.index = index
        self.symbol = symbol

class ScopeClasses():
    def __init__(self, *, run=None, generation=None, position=None):
        self.run = run or RunScope
        self.generation = generation or GenerationScope
        self.position = position or PositionScope

class ScopeBundle():
    def __init__(self, run, generation, position):
        self.run = run
        self.generation = generation
        self.position = position

class Generate():
    def __init__(self, lsystem: LSystem, depth: int, scope : ScopeClasses = None, seed : int = None):
        self.lsystem = lsystem
        self.depth = depth
        self.scope = scope or ScopeClasses()
        self.name = hash(self)
        self.seed = seed

    def run(self):
        ## Gather LSystem elements
        sentence = self.lsystem.sentence
        productions = self.lsystem.productions

        ## Update root Scope object and capture
        root = self.scope.run(self.name, self.lsystem, self.seed)

        for generation in range(self.depth):
            ## Update branch Scope object and capture
            branch = self.scope.generation(self.depth, generation, sentence)

            ## Build next sentence directly instead of storing rewrites first
            new_sentence = sentence.empty()

            for index, symbol in enumerate(sentence):
                ## Update leaf Scope object and capture
                leaf = self.scope.position(index, symbol)

                ## Retrieve production
                production = productions.get(symbol)

                ## Construct ScopeBundle to be passed to production
                package = ScopeBundle(root, branch, leaf)

                ## Apply production and combine immediately
                rewrite = production(symbol, package)
                new_sentence = new_sentence.combine(rewrite)

            ## Advance to the next generation
            sentence = new_sentence

        return sentence
            
def Run(generate: Generate):
    return generate.run()
