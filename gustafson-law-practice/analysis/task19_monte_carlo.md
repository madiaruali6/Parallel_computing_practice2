# Task 19 — Monte Carlo: The Ideal Weak-Scaling Workload

## Sources of non-zero α
1. **PRNG seeding / stream management.** Naïve shared-seed generation correlates streams; safe schemes: (a) counter-based generators (Philox, Threefry) — O(1) per stream, no coordination; (b) jump-ahead/leapfrog LCG, MRG32k3a streams — O(log skip) per stream, computed in parallel; (c) SplitMix/seed-sequencing — one serial master distributing P seeds: **O(P)** serial cost if done sequentially on rank 0 ⇒ α contribution ∝ P·t_seed. Prefer (a), cost 0 serial.
2. **Reductions** (sum, variance, histogram): tree: T_red = t_r·⌈log₂P⌉; linear (rank 0 receives from all): T_red = t_r·(P−1).
3. **Output serialisation / checkpoint**: single writer of R bytes at bandwidth B: R/B constant (if result size fixed) or ∝ P·(bytes per rank)/B if per-rank dumps are gathered.
4. **Initialisation**: geometry/cross-section tables loaded by one rank and broadcast (O(log P) with tree broadcast).
5. **Load imbalance** (variable path lengths, e.g. particle transport): adds idle time ∝ the tail of the path-length distribution; mitigate by dynamic batches.

## Quantifying reduction trees on S(P)
α_red = T_red/T_total; S(P) = P − α_total(P−1) (with α_total including α_red).
Example: T_total = 60 s per rank (constant work), t_r = 50 µs per reduction hop (small payload, latency-bound), P = 65 536 (16 levels).

| Reduction | T_red | α_red | S(P) loss α_red(P−1) | S(P) |
|---|---:|---:|---:|---:|
| binary tree (log₂ P = 16) | 0.80 ms | 1.33·10⁻⁵ | 0.87 | 65 535.1 |
| linear, rank 0 gathers (P−1 receives at 2 µs) | 131 ms | 2.18·10⁻³ | 143.1 | 65 392.9 |
| linear, 50 µs per message | 3.28 s | 5.46·10⁻² | 3579 | 61 957 |

(Check: 0.8e-3/60 = 1.33e-5; 65535·2e-6 = 0.131 s ⇒ 2.18e-3·65535 = 143.1.)

## Conclusions
* With tree reductions and counter-based PRNGs, α ≈ 10⁻⁵–10⁻⁴ and E(P) > 99.9 %: Monte Carlo is the textbook Gustafson workload.
* Linear collectives make α ∝ P, which transforms the problem into the C(P) = γP regime (Task 12): the speedup ceiling reappears. Algorithm choice for the reduction matters more than anything else.
* Statistical caveat: the *statistical error* falls as 1/√(PK), so fixed-time scaling improves accuracy by √P only — "speedup" is measured in samples, not in error reduction.
