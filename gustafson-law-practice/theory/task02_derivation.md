# Task 02 — Derivation of Gustafson's Scaled Speedup

**Notation.** On the P-core machine, the scaled problem runs for wall-clock time normalised to 1:
s = serial time, p = parallel time, **s + p = 1**. α ≡ s (the serial fraction observed on the *parallel* machine).

1. **Parallel-machine run.** One core executes the serial phase for time s; during p all P cores work concurrently for time p. (Line justification: definition of s, p.)
2. **Work done in the parallel phase.** Each of P cores performs p units of work, total P·p core-time-units of work. (Assumes the parallel phase scales perfectly: work ∝ P at constant time — Gustafson's fixed-time assumption.)
3. **Equivalent serial runtime.** One core must do the serial work (s) and all parallel work (P·p) one after another: T₁ = s + p·P.  (Assumes no cache/memory effects differ between runs.)
4. **Speedup = T₁ / T_P.** S(P) = (s + pP)/(s + p) = s + pP   since s + p = 1. ∎ (first form)
5. **Express with α.** p = 1 − s = 1 − α ⇒ S(P) = α + (1 − α)P.
6. **Expand.** α + P − αP = P − α(P − 1). Hence **S(P) = P − α(P − 1)**. ∎
7. **Check limits.** α = 0 ⇒ S = P (ideal). α = 1 ⇒ S = P − (P − 1) = 1 (fully serial). P = 1 ⇒ S = 1 − …: S = 1 − α·0 = 1 ✓. Slope dS/dP = 1 − α > 0: linear, no ceiling.
8. **Efficiency.** E = S/P = 1 − α(P−1)/P (→ 1−α).

**Note on normalisation.** Because the formula uses fractions of the parallel-machine run time, it is only meaningful with α measured there; see Task 03.
