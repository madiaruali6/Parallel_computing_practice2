# Task 08 — Amdahl vs. Gustafson at s = α = 0.08, P = 128

## Amdahl
S_A = 1/(s + (1−s)/P) = 1/(0.08 + 0.92/128) = 1/(0.08 + 0.0071875) = 1/0.0871875 = **11.4695**

## Gustafson
S_G = P − α(P−1) = 128 − 0.08·127 = 128 − 10.16 = **117.8400**

## Discrepancy
* Absolute: 106.3705
* Ratio S_G/S_A = **10.274×** (Gustafson ≈ 927 % higher than Amdahl).
* Amdahl is 90.3 % below Gustafson (relative to S_G).

## Divergence sweep
| P | Amdahl | Gustafson | S_G / S_A |
|---:|---:|---:|---:|
| 2 | 1.852 | 1.920 | 1.04 |
| 8 | 5.128 | 7.440 | 1.45 |
| 32 | 9.195 | 29.520 | 3.21 |
| 128 | 11.470 | 117.840 | 10.27 |
| 512 | 12.225 | 471.120 | 38.54 |
| 2048 | 12.430 | 1884.240 | 151.59 |
| 8192 | 12.482 | 7536.720 | 603.78 |

## Why they diverge
Amdahl's ceiling is 1/s = 12.50; its curve saturates (strong scaling: a fixed workload is sliced thinner, so the serial part dominates). Gustafson's grows linearly with slope (1−α)=0.92 (weak scaling: the parallel part grows with P while the serial part stays fixed in time). The models are not the same program at the same number: Amdahl's s is a fraction of the 1-core time of the fixed problem; Gustafson's α is a fraction of the P-core time of the scaled problem. Using one value for both (as prescribed) compares *workload-scaling policies*, not one workload. Divergence is unbounded: S_G/S_A → ∞ as P → ∞ (S_A is bounded, S_G ∼ 0.92·P).
