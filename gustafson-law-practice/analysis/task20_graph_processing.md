# Task 20 — Why Weak Scaling is Hard for Graph Analytics (BFS, PageRank on power-law graphs)

## Contrast with dense linear algebra
| Property | Dense GEMM / stencil | BFS / PageRank on power-law graphs |
|---|---|---|
| Arithmetic intensity | high (∼N/√cache flops per byte) | very low (≈1 edge ∼ 8–16 B moved per few ops) |
| Memory access | regular, prefetchable, cache-blocked | irregular, data-dependent, cache/TLB-hostile |
| Partitioning | geometric, balanced, surface ≪ volume | edge cuts large (small-world, no good separators) |
| Work per rank at fixed n | uniform | heavy-tailed: hubs with degree 10⁵–10⁶ |
| Communication | neighbour, O(n²) | all-to-all, ∼ cut edges ∝ m(1−1/P) |
| Synchronisation | one halo per step | per-level barrier (BFS), per-iteration global reduction (PageRank) |

## Mechanisms that break Gustafson's assumptions
1. **Work is not ∝ vertices.** BFS work ∼ edges visited, determined by the frontier — data dependent. Doubling the graph (with a Kronecker/R-MAT generator) increases diameter only slowly (∼log N), but the **frontier peaks in 2–3 levels** holding most of the edges ⇒ strongly bursty parallelism; most levels are tiny ⇒ per-level latency (barrier, allreduce) dominates: α ∼ (#levels · t_sync)/T.
2. **Load imbalance from power-law degrees:** with 1D vertex partitioning a rank owning a hub performs orders-of-magnitude more work; the slowest rank sets the time ⇒ effective serial fraction rises with P because the expected maximum of heavy-tailed loads grows ∼P^{1/(γ−1)}.
3. **Communication volume ∝ edges cut:** random partitions cut (1−1/P) of edges, i.e. nearly all edges become remote messages: comm/comp ratio does not improve with scale (unlike surface-to-volume). Bisection bandwidth, not per-node bandwidth, binds.
4. **Memory-latency bound:** per-core throughput limited by outstanding random loads; weak scaling is then a function of *message rate* (Graph500 reports TEPS, with efficiency typically falling below 50 % at 10⁴+ nodes).
5. **No natural constant-time problem size:** scaling vertices ∝ P changes degree distribution/diameter statistics; PageRank iterations to converge depend on spectral gap and are ≈ constant, which is the one favourable property.
6. **Global dependencies:** direction-optimising BFS needs global frontier counts; connected-component and shortest-path algorithms add data-dependent iterations.

## Mitigation
2D (checkerboard) partitioning (communication ∼ n/√P), degree-aware vertex delegation of hubs, hybrid top-down/bottom-up BFS, message coalescing and one-sided/asynchronous communication, vertex reordering for locality.

## Conclusion
In Gustafson terms, α(P) and C(P) are neither small nor constant for graph kernels; a constant-α fit is invalid and reported weak-scaling efficiency reflects network capability more than algorithm quality. Sun–Ni with G(P) ≪ P and the Task 12 model with γ·P-type communication describe them better.
