# Task 03 — The Serial-Fraction "Invariance Paradox": Frame of Reference

## The apparent contradiction
Amdahl: a serial fraction of only 1 % caps speedup at 100, so massive machines look pointless. Yet real codes achieve ~1000× on 1024 processors (Task 05). How can a non-zero serial fraction exist *and* not throttle scaling?

## Resolution: s and α are different quantities
* Amdahl's s = T_serial / (T_serial + T_parallel) measured on **1 processor with the fixed problem**: s = t_s/(t_s + t_p).
* Gustafson's α = t_s / (t_s + t_p′) measured on **P processors with the scaled problem**, where t_p′ is the *wall-clock* parallel time.

Relation: the scaled problem's 1-core parallel work is P·t_p′, hence the uniprocessor serial fraction of the *scaled* problem is
s_scaled = t_s / (t_s + P t_p′) = α / (α + (1−α)P).
Substituting into Amdahl for the scaled problem: S = 1/(s_scaled + (1 − s_scaled)/P). With s_scaled = α/(α+(1−α)P):
 s_scaled + (1 − s_scaled)/P = [α + (1−α)]/(α + (1−α)P) = 1/(α + (1−α)P)  ⇒ **S = α + (1−α)P = P − α(P−1)** — *exactly* Gustafson's law. ∎

So the two laws are consistent: Gustafson is Amdahl applied to a problem whose uniprocessor serial fraction s_scaled → 0 as P → ∞ (∼ α/((1−α)P)). The serial *time* is invariant (constant in seconds); the serial *fraction of the work* shrinks because the parallel work grows.

## Frame of reference
Measured on the parallel machine, α reports what the P-core run actually looked like — what a practitioner can observe — and implicitly encodes the problem size used. Measured on a uniprocessor, s is a property of one fixed (small) problem and cannot be extrapolated to scaled sizes. Using a uniprocessor s from a small problem to predict large-P behaviour thus yields spurious pessimism; using α from a P-core run to predict *much larger* P' requires that α stays constant (Task 12 shows when it does not).

## Caveat
α is only constant if the serial *time* stays constant as the problem grows. Serial work that scales with N (e.g., serial I/O ∝ N) makes α grow and recovers Amdahl-like behaviour.
