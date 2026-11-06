# Task 17 — 3D 7-Point Stencil: Surface-to-Volume under Weak Scaling

## Setup
Global domain N³ on a P^(1/3)×P^(1/3)×P^(1/3) rank grid; each rank owns n³ cells, n = N/P^(1/3).
Compute per rank per step ∝ n³ (≈8 flops/cell); halo data = 6 faces × n² points.

**Communication/computation ratio per rank: ρ = 6n²/n³ = 6/n.**

## Weak scaling (volume ∝ P)
Fix n (work per rank constant ⇒ runtime constant ⇒ Gustafson fixed-time). Then N = n·P^(1/3) and **ρ = 6/n is independent of P**: it neither improves nor degrades. With n = 64: ρ = 0.0938.
Strong scaling (fixed N₀ = 64): n = N₀/P^(1/3) ⇒ ρ = 6P^(1/3)/N₀, growing as P^(1/3) — the Amdahl-style degradation (last column).

| P | Weak: N = n·P^(1/3) | Per-rank cells | ρ weak | ρ strong (N₀=64) |
|---:|---:|---:|---:|---:|
| 1 | 64 | 64³ | 0.0938 | 0.0938 |
| 8 | 128 | 64³ | 0.0938 | 0.1875 |
| 64 | 256 | 64³ | 0.0938 | 0.3750 |
| 512 | 512 | 64³ | 0.0938 | 0.7500 |
| 4096 | 1024 | 64³ | 0.0938 | 1.5000 |

## α view
Per-rank halo time T_c = 6·t_s + t_w·6n² is independent of P (nearest-neighbour only) ⇒ α_comm = T_c/(T_c+T_comp) is constant ⇒ the stencil is a near-ideal Gustafson workload. Residual P-dependence: (i) global reductions (convergence/Δt): O(log P); (ii) network contention on non-ideal topologies; (iii) OS-noise amplification at barriers.

Proof of S/V: for a cube of side n, S/V = 6n²/n³ = 6/n, independent of P at fixed n. ∎
