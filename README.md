# lsystems

A small, compositional Python library for defining and generating **L-systems**.

This project is built around a simple idea:

* a **sentence** is an iterable monoidal container of symbols,
* a **production** rewrites one symbol into a new sentence,
* a **generator** applies productions across generations,
* and a **scope system** carries contextual information into each rewrite.

The result is a compact framework for deterministic, stochastic, and context-sensitive rewriting that is already useful for procedural generation, grammar experiments, and generative art pipelines.

---

# Current status

Implemented now:

* deterministic productions
* stochastic productions
* context-sensitive productions
* precedence-based production composition
* generic sentence protocol
* string-backed and tuple-backed sentence types
* scoped generation with run / generation / position context
* fallback identity rewrites for symbols without explicit productions

Planned next:

* interpreters (for example turtle or geometry backends)
* richer reproducible randomness via scoped RNGs
* tests and more examples

---

# Why this project exists

Most L-system examples are written as one-off scripts over strings. That is fine for a toy system, but it becomes limiting when you want to:

* swap out the underlying sentence representation,
* attach contextual information to rewrites,
* mix deterministic and stochastic rules,
* experiment with non-string symbol types,
* or treat rewriting as part of a larger compositional system.

`lsystems` tries to keep the core model small while making those extensions natural.

---

# Design overview

The package is centered on four concepts.

## 1. `Sentence`

A sentence is any type that behaves like an iterable sequence of symbols and supports a monoidal interface:

* `empty()`
* `lift(symbol)`
* `combine(other)`
* `clone()`

This lets the generator stay generic. A rewrite step does not care whether it is operating on a `str`, a `tuple`, or some future structured sentence type.

Currently included:

* `lsystems.sentences.string.String`
* `lsystems.sentences.tuple.Tuple`

---

## 2. `Production`

A production is anything callable with the shape:

```python
production(symbol, scope) -> Sentence
```

This is intentionally minimal. It means a production can be:

* a constant rewrite
* a stochastic chooser
* a context-sensitive rule
* a parametric rule
* or a production that inspects the current run, generation, or position

---

## 3. `Productions`

`Productions` stores the mapping from symbols to production objects.

If a symbol has no registered production, the system falls back to an identity-style rewrite by lifting the symbol back into the sentence type.

In other words, unspecified symbols persist automatically.

---

## 4. `Generate`

`Generate` performs the derivation over a fixed number of generations.

For each generation:

1. iterate through the current sentence
2. retrieve the production for each symbol
3. build a `ScopeBundle` for that symbol
4. rewrite each symbol into a sentence
5. combine all rewrites into the next sentence

This makes the derivation pipeline explicit and easy to extend.

---

# Package layout

```
src/lsystems/
├── __main__.py
├── generate.py
├── lsystem.py
├── productions/
│   ├── productions.py
│   ├── static.py
│   ├── stochastic.py
│   ├── precedence.py
│   └── context.py
├── protocols/
│   ├── production.py
│   └── sentence.py
└── sentences/
    ├── string.py
    └── tuple.py
```

---

# Installation

From the project root:

```bash
pip install .
```

For development:

```bash
pip install -e .[dev]
```

---

# Quick start

```python
from lsystems.sentences.string import String
from lsystems.productions.static import Static
from lsystems.productions.productions import Productions
from lsystems.lsystem import LSystem
from lsystems.generate import Generate

sentence = String("X")

productions = Productions(String)
productions.add("X", Static(String("F+[[X]-X]-F[-FX]+X")))
productions.add("F", Static(String("FF")))

alphabet = set("FX+-[]")
lsys = LSystem(alphabet, productions, sentence)

result = Generate(lsys, depth=2).run()
print(result)
```

---

# Production types

## Static productions

`Static` always returns the same rewrite sentence.

```python
from lsystems.productions.static import Static
from lsystems.sentences.string import String

Static(String("AB"))
```

---

## Stochastic productions

`Stochastic` selects a rewrite using weighted probabilities.

```python
from lsystems.productions.stochastic import Stochastic
from lsystems.sentences.string import String

rule = Stochastic()
rule.add(3, String("AA"))
rule.add(1, String("AB"))
```

Internally this is stored using cumulative cutoffs and sampled with `bisect`.

---

## Precedence productions

`Precedence` allows multiple production strategies to be layered.

Productions are evaluated in order, and the first one that resolves is used.

```python
from lsystems.productions.precedence import Precedence
from lsystems.productions.static import Static
from lsystems.productions.stochastic import Stochastic
from lsystems.sentences.string import String

context_rule = Static(String("X"))

fallback = Stochastic()
fallback.add(3, String("AA"))
fallback.add(1, String("AB"))

production = Precedence(
    context_rule,
    fallback
)
```

This makes it easy to express rules like:

```
context rule
↓
stochastic rule
↓
identity
```

---

## Context-sensitive productions

`ContextSensitive` matches rules based on surrounding symbols.

Example rule:

```
empty > A < B → X
```

Meaning:

> rewrite `A` to `X` when it appears at the start of the sentence and is followed by `B`.

Example implementation:

```python
from lsystems.productions.context import ContextSensitive
from lsystems.sentences.string import String

rule = ContextSensitive(0, 1)
rule.add(String(""), String("B"), String("X"))
```

If no rule matches the surrounding context, the symbol is preserved.

---

## Variational context-sensitive productions

`VariationalContextSensitive` combines several context rules of different widths.

Wider contexts automatically take precedence.

Example:

```
CA > B < CA → Z
A  > B < A  → Y
empty > B < A → X
```

Example implementation:

```python
from lsystems.productions.context import (
    ContextSensitive,
    VariationalContextSensitive
)
from lsystems.sentences.string import String

ctx_22 = ContextSensitive(2,2)
ctx_22.add(String("CA"), String("CA"), String("Z"))

ctx_11 = ContextSensitive(1,1)
ctx_11.add(String("A"), String("A"), String("Y"))

ctx_01 = ContextSensitive(0,1)
ctx_01.add(String(""), String("A"), String("X"))

production = VariationalContextSensitive(
    ctx_22,
    ctx_11,
    ctx_01
)
```

---

# Scope system

Each production receives a `ScopeBundle` containing:

* `run`
* `generation`
* `position`

These scopes provide contextual information during rewriting.

### Run scope

Created once for the full derivation.

Fields:

* `name`
* `lsystem`
* `seed`
* `rng`

---

### Generation scope

Created once per generation.

Fields:

* `depth`
* `generation`
* `sentence`

---

### Position scope

Created once per symbol.

Fields:

* `index`
* `symbol`

---

# Running the examples

The repository includes several working examples in:

```
src/lsystems/__main__.py
```

Run them with:

```bash
python -m lsystems
```

---

# Development philosophy

The project aims for a balance:

* **small enough** to understand completely
* **generic enough** to extend
* **compositional enough** to integrate with other systems

---

# Future directions

Possible extensions include:

* parametric symbols
* turtle graphics interpreters
* grammar-driven production synthesis
* parser-based rule matching
* additional sentence container types

---

# License

See `LICENSE`.

