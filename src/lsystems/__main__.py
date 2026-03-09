from lsystems.sentences.string import String
from lsystems.sentences.tuple import Tuple
from lsystems.productions.static import Static
from lsystems.productions.stochastic import Stochastic
from lsystems.productions.precedence import Precedence
from lsystems.productions.context import ContextSensitive, VariationalContextSensitive
from lsystems.productions.generation import Generation
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
print()

# ============================================================
# Example 2: stochastic plant-ish branching
# ============================================================

sentence = String("X")

productions = Productions(String)

x_prod = Stochastic()
x_prod.add(10, Static(String("F[+X]F[-X]+X")))
x_prod.add(8,  Static(String("F[-X]F[+X]-X")))
x_prod.add(6,  Static(String("F[+X]-X")))
x_prod.add(6,  Static(String("F[-X]+X")))
x_prod.add(4,  Static(String("F[X]+X")))
x_prod.add(3,  Static(String("F[-X]-X")))
x_prod.add(2,  Static(String("FX")))

f_prod = Stochastic()
f_prod.add(12, Static(String("FF")))
f_prod.add(6,  Static(String("F")))
f_prod.add(4,  Static(String("F+F")))
f_prod.add(4,  Static(String("F-F")))
f_prod.add(2,  Static(String("FF[+F]")))
f_prod.add(2,  Static(String("FF[-F]")))

productions.add("X", x_prod)
productions.add("F", f_prod)

alphabet = set("FX+-[]")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=3)

print("Example 2")
print(gen.run())
print()


# ============================================================
# Example 3: stochastic algae / rewriting toy
# ============================================================

sentence = String("A")

productions = Productions(String)

a_prod = Stochastic()
a_prod.add(10, Static(String("AB")))
a_prod.add(7,  Static(String("BA")))
a_prod.add(5,  Static(String("AA")))
a_prod.add(4,  Static(String("A[B]A")))
a_prod.add(3,  Static(String("A+A")))
a_prod.add(2,  Static(String("A-A")))

b_prod = Stochastic()
b_prod.add(10, Static(String("A")))
b_prod.add(8,  Static(String("BB")))
b_prod.add(6,  Static(String("BA")))
b_prod.add(4,  Static(String("B[A]")))
b_prod.add(3,  Static(String("B+B")))
b_prod.add(2,  Static(String("B-B")))

productions.add("A", a_prod)
productions.add("B", b_prod)

alphabet = set("AB+-[]")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=4)

print("Example 3")
print(gen.run())
print()


# ============================================================
# Example 4: stochastic corridor / geometric doodle
# ============================================================

sentence = String("G")

productions = Productions(String)

g_prod = Stochastic()
g_prod.add(12, Static(String("F+G")))
g_prod.add(10, Static(String("F-G")))
g_prod.add(8,  Static(String("F[+G]")))
g_prod.add(8,  Static(String("F[-G]")))
g_prod.add(6,  Static(String("F[+G][-G]")))
g_prod.add(4,  Static(String("FG")))
g_prod.add(2,  Static(String("G")))

f_prod = Stochastic()
f_prod.add(10, Static(String("FF")))
f_prod.add(7,  Static(String("F")))
f_prod.add(5,  Static(String("F+F")))
f_prod.add(5,  Static(String("F-F")))
f_prod.add(3,  Static(String("F[+F]")))
f_prod.add(3,  Static(String("F[-F]")))

productions.add("G", g_prod)
productions.add("F", f_prod)

alphabet = set("FG+-[]")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=5, seed=None)

print("Example 4")
print(gen.run())
print()

# ============================================================
# Example 5: precedence = context first, stochastic fallback
# ============================================================

sentence = String("ABA")

productions = Productions(String)

a_ctx = ContextSensitive(0, 1)
a_ctx.add(String(""), String("B"), Static(String("X")))   # empty > A < B

a_stoch = Stochastic()
a_stoch.add(3, Static(String("AA")))
a_stoch.add(1, Static(String("AB")))

a_prod = Precedence(a_ctx, a_stoch)

b_prod = Static(String("B"))

productions.add("A", a_prod)
productions.add("B", b_prod)

alphabet = set("ABX")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=1, seed=7)

print("Example 5")
print(gen.run())
print()

# ============================================================
# Example 6: fixed-width context sensitive production
# ============================================================

sentence = String("ABAA")

productions = Productions(String)

a_ctx = ContextSensitive(0, 1)
a_ctx.add(String(""), String("B"), Static(String("X")))   # empty > A < B

productions.add("A", a_ctx)

alphabet = set("ABX")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=1)

print("Example 6")
print(gen.run())
print()

# ============================================================
# Example 7: variational context sensitive production
# ============================================================

sentence = String("ABAA")

productions = Productions(String)

ctx_11 = ContextSensitive(1, 1)
ctx_11.add(String("B"), String("A"), Static(String("Y")))   # B > A < A

ctx_01 = ContextSensitive(0, 1)
ctx_01.add(String(""), String("B"), Static(String("X")))    # empty > A < B

a_var = VariationalContextSensitive(
    ctx_11,
    ctx_01,
    auto_order=True,
)

productions.add("A", a_var)
productions.add("B", Static(String("B")))
productions.add("X", Static(String("X")))
productions.add("Y", Static(String("Y")))

alphabet = set("ABXY")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=1)

print("Example 7")
print(gen.run())
print()

# ============================================================
# Example 8: guarded burst
# ============================================================

sentence = String("ABABA")

productions = Productions(String)

a_ctx = ContextSensitive(0, 1)
a_ctx.add(String(""), String("B"), Static(String("X")))   # empty > A < B

a_stoch = Stochastic()
a_stoch.add(5, Static(String("AA")))
a_stoch.add(3, Static(String("AB")))
a_stoch.add(2, Static(String("A+A")))

a_prod = Precedence(a_ctx, a_stoch)

productions.add("A", a_prod)
productions.add("B", Static(String("B")))
productions.add("X", Static(String("X")))
productions.add("+", Static(String("+")))

alphabet = set("ABX+")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=2, seed=11)

print("Example 8")
print(gen.run())
print()

# ============================================================
# Example 9: competing contexts
# ============================================================

sentence = String("CABACABA")

productions = Productions(String)

ctx_22 = ContextSensitive(2, 2)
ctx_22.add(String("CA"), String("CA"), Static(String("Z")))   # CA > B < CA

ctx_11 = ContextSensitive(1, 1)
ctx_11.add(String("A"), String("A"), Static(String("Y")))     # A > B < A

ctx_01 = ContextSensitive(0, 1)
ctx_01.add(String(""), String("A"), Static(String("X")))      # empty > B < A

b_var = VariationalContextSensitive(
    ctx_22,
    ctx_11,
    ctx_01,
    auto_order=True,
)

productions.add("A", Static(String("A")))
productions.add("B", b_var)

alphabet = set("ABCXYZ")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=1)

print("Example 9")
print(gen.run())
print()

# ============================================================
# Example 10: edge ignition
# ============================================================

sentence = String("FFFF")

productions = Productions(String)

left_edge = ContextSensitive(0, 1)
left_edge.add(String(""), String("F"), Static(String("L")))

right_edge = ContextSensitive(1, 0)
right_edge.add(String("F"), String(""), Static(String("R")))

middle = ContextSensitive(1, 1)
middle.add(String("F"), String("F"), Static(String("M")))

f_prod = VariationalContextSensitive(
    middle,
    left_edge,
    right_edge,
    auto_order=True,
)

productions.add("F", f_prod)
productions.add("L", Static(String("L")))
productions.add("M", Static(String("M")))
productions.add("R", Static(String("R")))

alphabet = set("FLMR")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=1)

print("Example 10")
print(gen.run())
print()

# ============================================================
# Example 11: contextual vine
# ============================================================

sentence = String("FXFXX")

productions = Productions(String)

x = ContextSensitive(1, 1)
x.add(String("F"), String("F"), Static(String("F[+X]-X")))
x.add(String("X"), String("X"), Static(String("F[-X]+X")))

x_default = Static(String("FX"))

x_prod = Precedence(
    x,
    x_default,
)

f_stoch = Stochastic()
f_stoch.add(5, Static(String("FF")))
f_stoch.add(2, Static(String("F")))
f_stoch.add(1, Static(String("F+F")))

productions.add("X", x_prod)
productions.add("F", f_stoch)
productions.add("+", Static(String("+")))
productions.add("-", Static(String("-")))
productions.add("[", Static(String("[")))
productions.add("]", Static(String("]")))

alphabet = set("FX+-[]")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=2, seed=19)

print("Example 11")
print(gen.run())
print()

# ============================================================
# Example 12: symbol chemistry
# ============================================================

sentence = String("ABABACABA")

productions = Productions(String)

a_ctx1 = ContextSensitive(1, 1)
a_ctx1.add(String("C"), String("B"), Static(String("Q")))   # C > A < B
a_ctx1.add(String("B"), String("C"), Static(String("R")))   # B > A < C

a_prod = VariationalContextSensitive(
    a_ctx1,
    fallback=Stochastic(),
    auto_order=True,
)

# fill stochastic fallback
a_prod.productions[-1].add(4, Static(String("AA")))
a_prod.productions[-1].add(2, Static(String("AB")))
a_prod.productions[-1].add(1, Static(String("A")))

productions.add("A", a_prod)
productions.add("B", Static(String("BC")))
productions.add("C", Static(String("C")))
productions.add("Q", Static(String("Q")))
productions.add("R", Static(String("R")))

alphabet = set("ABCQR")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=2, seed=5)

print("Example 12")
print(gen.run())
print()

# ============================================================
# Example 13: generation-indexed production
# ============================================================

sentence = String("A")

productions = Productions(String)

a_gen = Generation(fallback=Static(String("A")))
a_gen.add(0, Static(String("AB")))
a_gen.add(1, Static(String("BA")))
a_gen.add(2, Static(String("AA")))

productions.add("A", a_gen)
productions.add("B", Static(String("B")))

alphabet = set("AB")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=4)

print("Example 13")
print(gen.run())
print()

# ============================================================
# Example 14: nested Generation inside Precedence
# ============================================================

sentence = String("A")

productions = Productions(String)

a_gen = Generation(fallback=None)
a_gen.add(0, Static(String("AB")))
a_gen.add(1, Static(String("BA")))
a_gen.add(2, Static(String("AA")))

a_prod = Precedence(
    a_gen,
    Static(String("A")),   # fallback if Generation returns None
)

productions.add("A", a_prod)
productions.add("B", Static(String("BB")))

alphabet = set("AB")

lsys = LSystem(alphabet, productions, sentence)
gen = Generate(lsys, depth=5)

print("Example 14")
print(gen.run())
print()
