# Task 14 — Isoefficiency View of Gustafson Scaling

**Definitions (Grama, Gupta, Kumar).** Sequential work W (time of best serial algorithm), parallel time T_P, overhead T_o(W,P) = P·T_P − W, efficiency E = W/(W + T_o) = 1/(1 + T_o/W). Constant E requires **W = K·T_o(W,P)** with K = E/(1−E); the solution W = f(P) is the isoefficiency function.

## Gustafson's program
Per unit time of the P-core run: serial phase s (one core busy, P−1 idle) and parallel phase p (all busy). Work W = s + pP. T_P = s + p = 1.
T_o = P·1 − (s + pP) = P(s+p) − s − pP = **s(P−1)**.

Then E = W/(W + T_o) = (s + pP)/(s + pP + s(P−1)) = (s+pP)/(sP + pP) = (s + pP)/P ✓ (= S/P).

## Isoefficiency function
Required: W = K·T_o = K s (P−1) ⇒ **W = Θ(P)** — work must grow *linearly* in P. Gustafson's rule sets W(P) = s + pP = Θ(P), so it **satisfies the isoefficiency relation exactly** with s constant: the scaling is *iso-efficient up to the constant (1−α) bound*; E → 1−α (Task 04). Check: at W = s + pP, T_o/W = s(P−1)/(s+pP) → s/p, constant ⇒ E → 1/(1 + s/p) = p = 1−α ✓ (since s + p = 1).

## Critique
* Θ(P) is the **best possible** isoefficiency (a lower bound for any parallel system: W = Ω(P) is needed to keep P processors busy), i.e. a perfectly scalable system. Amdahl's fixed W has T_o = (P−1)·s·W (idle cores during the serial part), so T_o/W grows linearly in P: holding E would need s → 0 for fixed W, i.e. there is no problem-size growth rule inside the fixed-size model and E → 0.
* Gustafson's law hides the real difficulty: it *assumes* T_o ∝ P·(const), i.e. overhead independent of W's growth. In real systems T_o includes communication: T_o = Θ(P log P) (tree reductions) ⇒ W = Θ(P log P); T_o = Θ(P^{3/2}) (2D-mesh all-to-all) ⇒ W = Θ(P^{3/2}). Then holding per-processor work constant (Gustafson) *loses* efficiency; one must grow it as log P (P^{1/2}).
* Practical: isoefficiency tells *how fast* the problem must grow; Gustafson tells what speedup you get if you grow it at the pace that keeps T constant. They coincide only when T_o = Θ(P).
