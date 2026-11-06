# Task 06 — Parametric Speedup, α = 0.04

Formulas: S(P) = P − α(P−1), E(P) = S(P)/P = 1 − α(P−1)/P. Last column = "lost cores" α(P−1) (cores' worth of capacity idle during the serial phase).

| P | S(P) | E(P) | Lost cores α(P−1) |
|---:|---:|---:|---:|
| 16 | 15.4000 | 0.9625 | 0.6000 |
| 64 | 61.4800 | 0.9606 | 2.5200 |
| 256 | 245.8000 | 0.9602 | 10.2000 |
| 1024 | 983.0800 | 0.9600 | 40.9200 |
| 4096 | 3932.2000 | 0.9600 | 163.8000 |
| 16384 | 15728.6800 | 0.9600 | 655.3200 |

## Worked example (P = 16)
S = 16 − 0.04·15 = 16 − 0.6 = 15.4; E = 15.4/16 = 0.9625.

## Evaluation
* Efficiency does **not** collapse as P grows exponentially: it falls from 96.25 % (P=16) to 96.00 % (P=16384) because E(P) → 1 − α = 0.96 monotonically from above.
* Total efficiency loss across a 1024× increase in cores is only ≈0.2 percentage points. Almost all degradation happens at small P (E(1)=1 → E(16)=0.9625).
* Absolute waste grows linearly (α(P−1) cores idle: 0.6 → 655.3), yet is a constant fraction of the machine.
* Caveat: this holds only if α stays constant (see Task 12 for the communication-penalty model).
