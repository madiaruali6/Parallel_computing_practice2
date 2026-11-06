# Task 15 — Energy under Gustafson Scaling

## Model
Per node: P_active when computing, P_idle when waiting (static + idle dynamic). Fixed wall-clock T, normalised serial/parallel split s + p = 1 (α = s). Interconnect/uncore power ignored (add as P_net·P·T if needed).

**P-core run** (scaled problem, W = s + pP units):
E_P = T[ s(P_active + (P−1)P_idle) + p·P·P_active ]
   = T[ P_active(s + pP) + P_idle·s(P−1) ].
(First term = energy of useful work, second = energy burned idling during the serial phase.)

**1-core run, same wall-clock T** (can only do the baseline problem, W = 1 unit): E_1 = T·P_active (the core is busy the whole time).

## Energy per unit of work (efficiency of energy)
e_P = E_P / W = T·[P_active + P_idle·s(P−1)/(s + pP)] → T·[P_active + P_idle·α/(1−α)] as P → ∞.
e_1 = T·P_active.
Ratio e_P/e_1 = 1 + (P_idle/P_active)·α(P−1)/(P − α(P−1)) → 1 + (P_idle/P_active)·α/(1−α).

Example: P_idle/P_active = 0.4 (typical server idle ≈ 40–60 % of load power), α = 0.04 ⇒ penalty → 1 + 0.4·0.0417 = **1.017** (+1.7 %). With α = 0.2: 1 + 0.4·0.25 = 1.10.

## Total energy (not per work)
E_P/E_1 = (s + pP) + (P_idle/P_active)·s(P−1) ≈ S(P) + (P_idle/P_active)·α(P−1): total energy rises ∼ P, roughly in proportion to the speedup. **Equal wall-clock time ⇒ P cores burn ≈ S(P)× more energy but deliver S(P)× more work**; energy per result is essentially unchanged, rising only through idle power during serial phases.

## Insights
* The scaling is *energy-proportional* only if P_idle ≪ P_active or α small. Low-power idle states (race-to-idle, DVFS during serial/wait phases) directly reduce the second term.
* Compared with Amdahl strong scaling (fixed W, T shrinking): E = P·T_P·… grows because static power is paid over P cores for the whole run; energy per job is P·T_P·P_active-ish (all P nodes powered for T_P ≥ s·T₁), so with S bounded by 1/s the energy per job grows ∼P — the Amdahl regime is energy-inefficient while Gustafson's is not.
* If the baseline problem were run on 1 core for the *time needed* to do the P-times larger problem, wall-clock would be S(P)·T; energy would be E = S(P)·T·P_active ⇒ same as the active part of E_P: the P-core run costs only the extra idle term.
