# Feasible Edge Replacements — Algorithmic Companion to [1]

This repository is the algorithmic companion to the paper [1]. It provides a Python implementation of the permutation-factoring algorithms described in Section 5 of that paper, applied to the recursive family of Fibonacci-type trees introduced therein.

> **Note:** The `Fer` class and general amoeba methods in this repository have since been greatly expanded. For a more complete and actively maintained library, see the [FerGroup repository](https://github.com/tonamatos/FerGroup) and its [documentation](https://fergroup.research.wiederhold.dev/). This repository exists solely as a research artifact for the paper cited below.

---

## Algorithms

The main contribution of this codebase is the recursive implementation of the stem-symmetric factoring algorithm (Section 5 of [1]):

- Given a permutation $\sigma$ of a **stem-symmetric** amoeba $G_k$ from a recursive family, the algorithm produces a sequence of feasible edge replacements whose composition maps $G_k$ to $\sigma(G_k)$.
- The algorithm runs in $\Theta(n^2)$ time, where $n$ is the order of $G_k$. An improved $O(n\log n)$ algorithm is presented in the author's PhD thesis.
- The factoring is carried out recursively on the structure of the tree, using a fixed set of base cases computed up to $k = 4$.

The implementation in `main.py` applies this algorithm to the Fibonacci-type trees $T_k$ defined in `treebonacci.py`.

---

## Structure

| File | Description |
|------|-------------|
| `main.py` | Runs the stem-symmetric algorithm on $T_k$ for a given input permutation |
| `treebonacci.py` | Constructs the recursive family of Fibonacci-type trees and their structural parameters |
| `amoebas.py` | Graph-theoretic utilities: Cayley graph factorization, Fer generators, amoeba verification |
| `feasible_edge_replacement.py` | `Fer` class: sequences of feasible edge replacements with permutation composition |

---

## Setup

Requires Python 3.8+.

```bash
git clone https://github.com/tonamatos/Feasible-Edge-Replacements.git
cd Feasible-Edge-Replacements
pip install -r requirements.txt
```

---

## Running

```bash
python main.py
```

This runs the algorithm on a random permutation of $T_6$ (the Fibonacci-type tree at level $k=6$, with $2F_6 = 16$ vertices). To change the input, edit the `k` and `permutation` variables in `main.py`. The output is the resulting sequence of feasible edge replacements.

To verify correctness of the output, call `fer_verifier` from `amoebas.py`:

```python
from amoebas import fer_verifier
import treebonacci as trb
T = trb.Treebonacci(k)
fer_verifier(T[k], known_fer)
```

---

## Mathematical background

A *feasible edge replacement* (`Fer`) $(e \to g)$ of a graph $G$ is a pair of edges such that $G - e + g \cong G$. A graph is an *amoeba* if any isomorphic copy can be reached by a sequence of Fers. For full definitions see [2].

Paper [1] proves that the Fibonacci-type trees $T_k$ are amoebas and provides an efficient algorithm to factor any permutation into Fers by exploiting the recursive (stem-symmetric) structure of the family.

---

## References

[1] Eslava, L., Hansberg, A., Matos-Wiederhold, T., Ventura, D. *New recursive constructions of amoebas and their balancing number*. **Aequationes Mathematicae** 99 (2025), 1265–1299. [arXiv:2311.17182](https://arxiv.org/abs/2311.17182)

[2] Caro, Y., Hansberg, A., Montejano, A. *Graphs isomorphisms under edge-replacements and the family of amoebas*. **Electronic Journal of Combinatorics** 30(3) P3.9 (2023). [Link](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i3p9/pdf)

---

**Author:** Tonatiuh Matos-Wiederhold, Department of Mathematics, University of Toronto.
