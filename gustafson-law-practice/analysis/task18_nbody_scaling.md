# Task 18 — N-body: All-Pairs vs. Barnes–Hut under Fixed-Time Scaling

Let t_f = time per pairwise interaction; constant time per step T₀ on one core with N₀ particles.

## Direct all-pairs, O(N²)
Per-rank compute ≈ t_f N²/P (each rank owns N/P particles, interacts with all N; data must be circulated: all-gather/ring, N words per rank).
Fixed time: N²/P = N₀² ⇒ **N = N₀√P**. (P = 100 ⇒ only 10× more particles.)
Communication per rank: N words ∼ √P·N₀, vs. compute N₀² fixed ⇒ comm/comp ∼ √P/N₀ **grows as √P**: α_comm ↑. Serial/parallel ratio: serial I/O/setup ∼ O(N) ∼ √P grows too, while parallel time is pinned by construction. So α(P) = O(N)/(T) ∼ √P·c — α is *not* constant and Gustafson's constant-α formula over-estimates. Total work ∝ N² = N₀²P (linear in P: this is what fixed time buys), but *problem size* N grows only √P, so "scaled speedup" is realised as particles-count increase of √P.

## Barnes–Hut, O(N log N)
Per-rank compute ≈ t_f c (N/P)·log N (tree traversal θ-criterion; tree build is O(N log N) and often partly serial/replicated top levels).
Fixed time: (N/P) log N = N₀ log N₀ ⇒ N ≈ P·N₀·log N₀/log N ≈ **P N₀ / (1 + log P/ log N₀)**, i.e. N = Θ(P/ log P) (nearly linear, much better than √P).
Serial parts: top-of-tree construction/replication ∼ O(P·log) or O(log N) per rank; global tree build (if not parallel) O(N log N)·(1/P) after distribution; load-balancing (space-filling curves, sorting) O(N/P log N). Communication of "essential tree" ∼ O((N/P)^{2/3}) or O(log N) per rank — surface-to-volume as in Task 17.
α_BH(P) ∼ (serial top-tree + collective) / T ∼ (log P) / T₀ — grows only logarithmically.

## Comparison
| | All-pairs | Barnes–Hut |
|---|---|---|
| N(P) at fixed time | N₀ P^{1/2} | ≈ N₀ P/log P |
| Per-rank comm | O(N) = O(√P) | O(N/P)^{2/3} ≈ const |
| α(P) | ∼ √P (rapidly worsening) | ∼ log P (mild) |
| Gustafson validity | Poor | Good (near-linear) |
Take-away: Gustafson's promise depends on *algorithmic complexity*; algorithms with O(N log N) complexity weak-scale almost as ideal problems, O(N²) ones do not (Task 13, Task 11 with G(P) = P²/…).
