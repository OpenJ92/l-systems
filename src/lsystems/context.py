class Context(Protocol)
    def evolve(self, sentence, index, generation):
        return self
