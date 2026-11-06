# Task 12 — Gustafson with a Communication-Overhead Term

## Model
Normalise the *ideal* P-core runtime to s + p = 1 (α = s). Real runtime adds a communication/synchronisation time C(P) ≥ 0 (in units of the ideal runtime) that grows with P and is absent on one core, C(1) = 0:

  T_P = s + p + C(P) = 1 + C(P)

The serial-equivalent work is unchanged, W₁ = s + pP. Hence

  **S_C(P) = (s + p·P) / (1 + C(P)) = [P − α(P−1)] / [1 + C(P)]**,  E_C(P) = E_G(P)/(1 + C(P)).

Candidates: C(P) = γ·log₂P (tree collectives, e.g. Allreduce), C(P) = γ·√P (2D-mesh diameter/bisection effects), C = γ·P (all-to-all/serialised collectives), where γ = (communication cost per unit)/(ideal runtime).

## Asymptotics (α fixed)
* C = γ log₂ P: S_C ∼ (1−α)P/(γ log₂P) ⇒ E → 0 like 1/log P (slowly). Weak scaling is "almost" preserved.
* C = γ√P: S_C ∼ (1−α)√P/γ ⇒ E ∼ P^{−1/2}; speedup grows only as √P.
* C = γP: S_C → (1−α)/γ — a **ceiling reappears** (an Amdahl-like bound, now from communication).

## Equivalent effective serial fraction
Setting S_C = P − α_eff(P−1) gives α_eff(P) = (P − S_C)/(P − 1). This is the quantity a regression fit (Task 23) reports; it *increases* with P if communication grows.

## Numerical example (α = 0.04, γ = 0.002)
| P | Gustafson S | with γlog₂P : S (E) | with γ√P : S (E) |
|---:|---:|---:|---:|
| 16 | 15.4 | 15.3 (0.955) | 15.3 (0.955) |
| 256 | 245.8 | 241.9 (0.945) | 238.2 (0.930) |
| 4096 | 3932.2 | 3840.0 (0.938) | 3486.0 (0.851) |
| 65536 | 62914.6 | 60963.8 (0.930) | 41610.2 (0.635) |

## Restoring weak scaling
(1) Overlap communication with computation so C_exposed ≪ C; (2) increase work per rank with P (raises p relative to C: isoefficiency, Task 14); (3) use hierarchical/tree algorithms (log P instead of √P or P).
