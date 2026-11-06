# Task 16 — GEMM Dimension Scaling under Gustafson

## Proof
Work W(N) = 2N³ flops. Ideal per-processor time on P cores: T = 2N³/(P·r), r = per-core flop rate.
Fixed-time requirement T(P) = T(1) with baseline N₀: 2N³/(P r) = 2N₀³/r
⇒ N³ = P·N₀³ ⇒ **N(P) = N₀·P^(1/3)**. ∎

Consequences: total matrix memory ∝ N² ∝ P^(2/3) grows *slower* than P, so per-node memory shrinks as P^(−1/3): GEMM is never memory-limited under fixed-time scaling. Dimension grows ×2 for 8× processors, ×10 for 1000×.

Baseline N₀ = 4096:

| P | N(P) | Work ratio W/W₀ | One N×N double matrix per processor |
|---:|---:|---:|---:|
| 1 | 4096 | 1 | 128.0 MiB |
| 8 | 8192 | 8 | 64.0 MiB |
| 27 | 12288 | 27 | 42.7 MiB |
| 64 | 16384 | 64 | 32.0 MiB |
| 125 | 20480 | 125 | 25.6 MiB |
| 512 | 32768 | 512 | 16.0 MiB |
| 1000 | 40960 | 1000 | 12.8 MiB |
| 4096 | 65536 | 4096 | 8.0 MiB |

## Caveat
2D algorithms (SUMMA) move O(N²/√P) words per processor; with N ∝ P^(1/3) this scales as P^(2/3−1/2) = P^(1/6), so communication time slowly *grows* and α is not exactly constant (Task 12).
