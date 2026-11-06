# Task 13 — When Gustafson Fails

Gustafson's premises: (i) parallel work can be enlarged P-fold at fixed per-processor work, (ii) runtime then stays constant, (iii) α is constant. Two algorithms break these.

## Case 1 — Conjugate-Gradient solve of a 3D Poisson problem (sparse iterative solver)
* Weak scaling: subdomain n³ per rank fixed, global N = n·P^{1/3}.
* **Per-iteration** time is constant (local SpMV + halo exchange), *but* the number of CG iterations needed for fixed tolerance grows with the condition number κ ∼ N², i.e. iterations ∼ √κ ∼ N ∼ P^{1/3}. Total time ∼ P^{1/3} ⇒ the **constant-runtime premise fails** even with perfect communication.
* Each iteration has 2 global dot products (Allreduce, ∼ log P latency) ⇒ α grows with P (Task 12).
* Numbers: P = 512 vs. 1: iterations ×8; with 2 reductions of ∼20 µs·log₂P each… runtime ratio ≫ 1. Gustafson's S = P − α(P−1) would predict near-linear scaling; the real *time to solution* is 8× longer. Fix: multigrid preconditioners (iteration count independent of N), which restores weak scaling at the cost of coarse-grid serialisation.

## Case 2 — 3D FFT (spectral methods; global transposes)
* Complexity N³ log N³ for an N³ grid; weak scaling N³ = P·n³ ⇒ work per rank ∼ n³·log(P n³): grows ∼ log P → runtime not constant.
* Pencil-decomposition transposes are **all-to-all**: each rank exchanges data with √P (pencil) or P (slab) peers; bisection bandwidth of the interconnect scales ∼ P^{2/3} on a 3D torus while data volume ∼ P ⇒ communication time grows ∼ P^{1/3}.
* Therefore α_eff ↑ with P: S/P decays; weak scaling collapses at large P, which is why large spectral codes plateau.

## Others (brief)
All-pairs N-body (work N² — Task 18), dense LU with partial pivoting (latency-bound pivot search, O(N) sequential steps), branch-and-bound with search-order anomalies.

## Why the premise breaks
The law implicitly assumes *work ∝ problem size ∝ P* (linear complexity and local dependencies). Superlinear complexity, growth of iteration counts, or global dependencies decouple "problem size" from "work per processor".
