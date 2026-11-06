# Task 11 — Gustafson vs. Sun–Ni Memory-Bounded Speedup

## Models (normalised: serial fraction s, parallel fraction p = 1 − s of the 1-core workload of the baseline problem)
Let G(P) = factor by which the **parallel workload** grows when memory grows P-fold (set by algorithm complexity vs. data size).

**Sun–Ni:** S_MB(P) = (s + p·G(P)) / (s + p·G(P)/P).

Special cases:
* G = 1 (fixed size): S = 1/(s + p/P) → **Amdahl**.
* G = P (work ∝ P): S = (s + pP)/(s + p) = s + pP → **Gustafson**.
* G > P (work grows faster than memory, e.g. dense GEMM/LU: memory N², work N³ ⇒ G = P^{3/2}): S_MB exceeds Gustafson's speedup (see below).

Exact for G = P^{3/2}: S = (s + pP^{3/2})/(s + pP^{1/2}) → P as P→∞. Gustafson gives (1−s)P, so Sun–Ni predicts a *higher* speedup (→P, i.e. serial fraction vanishes entirely) but at **increasing wall-clock time**: T_P/T_1 = (s + pG/P)/(s+p) ≈ p·P^{1/2} → ∞ (grows as P^{1/2}). The fixed-time assumption is violated.

## When does Gustafson mis-estimate?
| Condition | G(P) vs P | Gustafson vs. reality |
|---|---|---|
| Memory-filling with superlinear-complexity algorithm (GEMM, LU, N-body all-pairs, FFT∼N log N) | G > P | Predicted speedup is **under**-estimated for the memory-bounded problem, but the run time grows beyond fixed-time (user may not accept it). |
| Work grows slower than memory (e.g. sparse matvec ∝ memory, G = P — equal; or graph analytics with sublinear work per memory, caching) | G < P | Gustafson **over**-estimates: fixed-time scaling of the problem is not possible with the available memory / the problem cannot be enlarged P-fold. |
| Memory per node cap prevents P-fold growth (Task 10: 3D grid with CFL) | G<P in time | Over-estimate. |
| Communication/serial parts growing with P (Task 12) | — | Gustafson **over**-estimates (α not constant). |
| Super-linear cache effects (working set fits in cache at large P) | — | Real speedup can exceed Gustafson (under-estimate). |

## Critique
Gustafson's law is accurate when parallel work scales linearly with memory (stencils, particle-in-cell with local interactions, Monte Carlo). Sun–Ni is the more general tool because G(P) is derived from the algorithm's complexity-to-memory relation, making the assumption explicit. Gustafson's law always requires verifying that the scaled problem is useful to the user and fits memory (Task 10).
