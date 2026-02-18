from lsystems.sentences.string import String
from lsystems.sentences.tuple import Tuple
from lsystems.productions.static import Static
from lsystems.productions.productions import Productions
from lsystems.lsystem import LSystem
from lsystems.generate import Generate

## Example 1

# Start symbol
sentence = String("X")

# Productions (deterministic)
productions = Productions(String)
productions.add("X", Static(String("F+[[X]-X]-F[-FX]+X")))
productions.add("F", Static(String("FF")))

# Alphabet includes every symbol we might emit
alphabet = set("FX+-[]")

lsys = LSystem(alphabet, productions, sentence)

gen = Generate(lsys, depth=2)
result = gen.run()

print(result)
print(result == "FF+[[F+[[X]-X]-F[-FX]+X]-F+[[X]-X]-F[-FX]+X]-FF[-FFF+[[X]-X]-F[-FX]+X]+F+[[X]-X]-F[-FX]+X")

## Example 2

# Start symbol
sentence = Tuple((0,))

# Productions
productions = Productions(Tuple)
productions.add(0, Static(Tuple((0, 1))))
productions.add(1, Static(Tuple((1, 2))))
productions.add(2, Static(Tuple((2, 0))))

alphabet = {0, 1, 2}

lsys = LSystem(alphabet, productions, sentence)

gen = Generate(lsys, depth=3)
result = gen.run()

print(result)
print(result == (0,1,1,2,1,2,2,0))

## Example 3

from dataclasses import dataclass

@dataclass(frozen=True)
class DiagonalDuplicateUntil:
    limit: int  # stop when x+y >= limit

    def __call__(self, symbol, scope):
        x, y = symbol
        if x + y < self.limit:
            return Tuple((symbol, (x + 1, y + 1)))
        return Tuple((symbol,))  # identity


# Start: one coordinate-pair symbol
sentence = Tuple(((0, 0),))

# Production table (identity for unspecified symbols)
productions = Productions(Tuple)

rule = DiagonalDuplicateUntil(limit=3)
productions.add((0, 0), rule)
productions.add((1, 1), rule)
productions.add((2, 2), rule)

alphabet = {(0, 0), (1, 1), (2, 2)}

lsys = LSystem(alphabet, productions, sentence)

result = Generate(lsys, depth=4).run()

print(result)
print(result == ((0, 0), (1, 1), (1, 1), (2, 2), (1, 1), (2, 2), (2, 2), (1, 1), (2, 2), (2, 2), (2, 2)))

