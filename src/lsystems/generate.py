class RunScope():
    def __init__(self, name, lsystem):
        self.name = name
        self.lsystem = lsystem

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
    def __init__(self, lsystem: LSystem, depth: int, scope : ScopeClasses = None):
        self.lsystem = lsystem
        self.depth = depth
        self.scope = scope or ScopeClasses()
        self.name = hash(self)

    def run(self):
        ## Gather LSystem elements
        sentence = self.lsystem.sentence
        productions = self.lsystem.productions

        ## Update root Scope object and capture
        root = self.scope.run(self.name, self.lsystem)

        for generation in range(self.depth):
            ## Update branch Scope object and capture
            branch = self.scope.generation(self.depth, generation, sentence)

            rewrites = []
            for index, symbol in enumerate(sentence):
                ## Update leaf Scope object and capture
                leaf = self.scope.position(index, symbol)

                ## Retrieve production 
                production = productions.get(symbol)

                ## Construct ScopeBundle to be passed to production
                package = ScopeBundle(root, branch, leaf)

                ## Apply production to current symbol with ScopeBundle 
                ## access and append to rewrites :: List[Sentence]
                rewrites.append(production(symbol, package))

            ## Overwrite current sentence :: Sentence with Monoidal empty
            sentence = sentence.empty()
            for rewrite in rewrites:
                ## Apply Monoidal combine linearly. Successful exit of loop
                ## reconstitutes the results of above productions into the 
                ## current generation's sentence
                sentence = sentence.combine(rewrite)

            print(sentence, generation)
        
        return sentence
            
def Run(generate: Generate):
    return generate.run()
