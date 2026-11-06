# Task 10 — Memory Ceiling vs. Weak Scaling

## Model
M(P) = c·P with c ≤ 32 GiB per node. Grid memory M = b·N³ with b bytes per cell.
**Assumption (parameterisable in `gen_calcs.py`):** b = 48 B/cell (6 double-precision field arrays). 1 GiB = 2³⁰ B.

Max cells per node: 32·2³⁰/48 = 715,827,882 ≈ 7.158e+08.
**N_max(P) = ⌊(P·32·2³⁰ / b)^(1/3)⌋**

| Nodes P | Aggregate memory | Max cells | N_max | Memory used at N_max |
|---:|---:|---:|---:|---:|
| 1 | 32 GiB | 7.1583e+08 | 894 | 31.9 GiB |
| 64 | 2048 GiB | 4.5813e+10 | 3578 | 2047.7 GiB |
| 512 | 16384 GiB | 3.6650e+11 | 7156 | 16381.5 GiB |

## Interpretation
* 1 node: N ≈ 894. 64 nodes: N = 3578 (= 4× since 64^(1/3) = 4). 512 nodes: N = 7156 (= 8×).
* A 3D grid weak-scaled to fill memory grows linearly only as P^(1/3): 8× more nodes yields just 2× finer linear resolution. With a CFL limit (Δt ∝ Δx) work grows as P^(4/3), so memory-filling cannot hold wall-time constant (cf. Tasks 11, 13).
* Per-node memory stays at 32 GiB: the defining feature of memory-bounded scaling.
* If the application is not at the memory limit, Gustafson's fixed-time condition, not memory, decides N (Task 16).
