# Task 04 — Asymptotic Efficiency

## Gustafson
E_G(P) = S/P = [P − α(P−1)]/P = 1 − α + α/P.

**lim_{P→∞} E_G(P) = 1 − α.** Proof: α/P → 0 (constant α, P→∞) so E_G → 1 − α. ∎
E_G is strictly decreasing for α∈(0,1]: dE/dP = −α/P² < 0, bounded below by (1−α), above by E(1)=1.
Examples: α = 0.04 ⇒ 0.96; α = 0.2 ⇒ 0.8; α = 1 ⇒ E = 1/P → 0 (degenerate, fully serial).

## Amdahl
E_A(P) = S_A/P = 1/(sP + (1−s)).
**lim_{P→∞} E_A(P) = 0** for any s > 0 (denominator → ∞). Rate: E_A ∼ 1/(sP). Proof: sP → ∞. ∎
Number of cores at half efficiency: E_A = 1/2 ⇔ sP + 1 − s = 2 ⇔ P = (1+s)/s ≈ 1/s (for s = 0.05, P ≈ 21).

## Contrast
| | limit E(P→∞) | S(P→∞) | Meaning |
|---|---|---|---|
| Gustafson | 1 − α > 0 | ∼(1−α)P, unbounded | Machine stays usefully busy as long as work scales |
| Amdahl | 0 | → 1/s, bounded | Machine becomes mostly idle |

Deduction: under fixed-size scaling, efficiency inevitably vanishes; under fixed-time scaling, a constant fraction of the machine's capacity is always productive. The loss in Gustafson's model (α(P−1) idle cores) grows linearly but is a constant fraction of P.
