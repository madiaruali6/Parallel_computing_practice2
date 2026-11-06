# Task 09 — Multi-Component Workload

Fractions of *parallel-machine* execution time: A (I/O + broadcast) 2 %, B (boundary sync) 6 %, C (flux compute) 92 %.

## Classification (assumption stated explicitly)
* A: serial (disk I/O by one rank; parameter broadcast not parallelised in the baseline model).
* B: non-scaling overhead (time does not shrink with P) → counted in α, as the task intends.
* C: perfectly parallel and scaled with P.

**α = 0.02 + 0.06 = 0.08**, p = 0.92.

## Scaled speedup
| P | S(P) = P − 0.08(P−1) | E(P) |
|---:|---:|---:|
| 512 | 512 − 0.08·511 = **471.12** | 0.9202 |
| 2048 | 2048 − 0.08·2047 = **1884.24** | 0.9200 |

## Per-phase contribution to lost capacity (P=2048)
Idle cores caused by A: 0.02·2047 = 40.94; by B: 0.06·2047 = 122.82; total 163.76.
B causes 75 % of the loss: optimising halo exchange (overlap with compute, fewer syncs) is worth 3× more than I/O (parallel I/O alone would give α = 0.06 → S(2048) = 1925.18).

## Caveat
In a real stencil code B is not strictly serial (all ranks participate); it is a communication cost, which belongs in the Task 12 model C(P). Constant α is optimistic if B grows with P, pessimistic if B is overlapped with compute.
