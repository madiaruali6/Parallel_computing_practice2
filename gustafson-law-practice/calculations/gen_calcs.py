"""Generates calculations/task06..task10, task16, task17 markdown from exact formulas."""
import math, pathlib
D = pathlib.Path(__file__).parent
G = lambda P,a: P - a*(P-1)
A = lambda P,s: 1/(s+(1-s)/P)

# ---- Task 06
a=0.04; rows=[]
for P in [16,64,256,1024,4096,16384]:
    S=G(P,a); rows.append(f"| {P} | {S:.4f} | {S/P:.4f} | {a*(P-1):.4f} |")
(D/"task06_parametric_table.md").write_text(f"""# Task 06 — Parametric Speedup, α = 0.04

Formulas: S(P) = P − α(P−1), E(P) = S(P)/P = 1 − α(P−1)/P. Last column = "lost cores" α(P−1) (cores' worth of capacity idle during the serial phase).

| P | S(P) | E(P) | Lost cores α(P−1) |
|---:|---:|---:|---:|
""" + "\n".join(rows) + """

## Worked example (P = 16)
S = 16 − 0.04·15 = 16 − 0.6 = 15.4; E = 15.4/16 = 0.9625.

## Evaluation
* Efficiency does **not** collapse as P grows exponentially: it falls from 96.25 % (P=16) to 96.00 % (P=16384) because E(P) → 1 − α = 0.96 monotonically from above.
* Total efficiency loss across a 1024× increase in cores is only ≈0.2 percentage points. Almost all degradation happens at small P (E(1)=1 → E(16)=0.9625).
* Absolute waste grows linearly (α(P−1) cores idle: 0.6 → 655.3), yet is a constant fraction of the machine.
* Caveat: this holds only if α stays constant (see Task 12 for the communication-penalty model).
""")

# ---- Task 07
P=8192; S=7500
amax=(P-S)/(P-1)
sA=(1/7500-1/8192)/(1-1/8192)
(D/"task07_tolerable_serial.md").write_text(f"""# Task 07 — Maximum Tolerable Serial Fraction

Given P = {P}, requirement S(P) ≥ {S}.

## Derivation
S(P) = P − α(P−1) ≥ S_min
⇒ α(P−1) ≤ P − S_min
⇒ **α_max = (P − S_min)/(P − 1)**   (valid since P > 1)

## Numbers
α_max = ({P} − {S}) / ({P} − 1) = {P-S} / {P-1} = **{amax:.6f}** (≈ {amax*100:.3f} %)

## Verification
S({P}) at α_max = {P} − {amax:.6f}·{P-1} = {G(P,amax):.4f} ✓ (equals {S}).
Required efficiency: {S}/{P} = {S/P:.4f}.

## Remark
The bound is linear in α, so tolerance is generous: the serial phase may take up to ≈{amax*100:.2f} % of the *parallel-machine* wall-clock time.
For comparison, under Amdahl (uniprocessor-measured s) reaching S ≥ 7500 on 8192 cores would need s ≤ {sA:.3e} (≈{sA*100:.4f} %), about {amax/sA:.0f}× stricter.
""")

# ---- Task 08
s=0.08; P=128
sa=A(P,s); sg=G(P,s)
sweep="\n".join(f"| {p} | {A(p,s):.3f} | {G(p,s):.3f} | {G(p,s)/A(p,s):.2f} |" for p in [2,8,32,128,512,2048,8192])
(D/"task08_cross_divergence.md").write_text(f"""# Task 08 — Amdahl vs. Gustafson at s = α = 0.08, P = 128

## Amdahl
S_A = 1/(s + (1−s)/P) = 1/(0.08 + 0.92/128) = 1/(0.08 + 0.0071875) = 1/0.0871875 = **{sa:.4f}**

## Gustafson
S_G = P − α(P−1) = 128 − 0.08·127 = 128 − 10.16 = **{sg:.4f}**

## Discrepancy
* Absolute: {sg-sa:.4f}
* Ratio S_G/S_A = **{sg/sa:.3f}×** (Gustafson ≈ {(sg/sa-1)*100:.0f} % higher than Amdahl).
* Amdahl is {(sg-sa)/sg*100:.1f} % below Gustafson (relative to S_G).

## Divergence sweep
| P | Amdahl | Gustafson | S_G / S_A |
|---:|---:|---:|---:|
{sweep}

## Why they diverge
Amdahl's ceiling is 1/s = {1/s:.2f}; its curve saturates (strong scaling: a fixed workload is sliced thinner, so the serial part dominates). Gustafson's grows linearly with slope (1−α)=0.92 (weak scaling: the parallel part grows with P while the serial part stays fixed in time). The models are not the same program at the same number: Amdahl's s is a fraction of the 1-core time of the fixed problem; Gustafson's α is a fraction of the P-core time of the scaled problem. Using one value for both (as prescribed) compares *workload-scaling policies*, not one workload. Divergence is unbounded: S_G/S_A → ∞ as P → ∞ (S_A is bounded, S_G ∼ 0.92·P).
""")

# ---- Task 09
al=0.02+0.06
(D/"task09_multicomponent.md").write_text(f"""# Task 09 — Multi-Component Workload

Fractions of *parallel-machine* execution time: A (I/O + broadcast) 2 %, B (boundary sync) 6 %, C (flux compute) 92 %.

## Classification (assumption stated explicitly)
* A: serial (disk I/O by one rank; parameter broadcast not parallelised in the baseline model).
* B: non-scaling overhead (time does not shrink with P) → counted in α, as the task intends.
* C: perfectly parallel and scaled with P.

**α = 0.02 + 0.06 = {al:.2f}**, p = 0.92.

## Scaled speedup
| P | S(P) = P − 0.08(P−1) | E(P) |
|---:|---:|---:|
| 512 | 512 − 0.08·511 = **{G(512,al):.2f}** | {G(512,al)/512:.4f} |
| 2048 | 2048 − 0.08·2047 = **{G(2048,al):.2f}** | {G(2048,al)/2048:.4f} |

## Per-phase contribution to lost capacity (P=2048)
Idle cores caused by A: 0.02·2047 = {0.02*2047:.2f}; by B: 0.06·2047 = {0.06*2047:.2f}; total {al*2047:.2f}.
B causes 75 % of the loss: optimising halo exchange (overlap with compute, fewer syncs) is worth 3× more than I/O (parallel I/O alone would give α = 0.06 → S(2048) = {G(2048,0.06):.2f}).

## Caveat
In a real stencil code B is not strictly serial (all ranks participate); it is a communication cost, which belongs in the Task 12 model C(P). Constant α is optimistic if B grows with P, pessimistic if B is overlapped with compute.
""")

# ---- Task 10
BYTES=48  # 6 arrays x 8 B per cell
cap=32*2**30
cells_node=cap//BYTES
rows=[];Ns={}
for nodes in (1,64,512):
    tot=cells_node*nodes; N=int(math.floor(tot**(1/3)+1e-9)); Ns[nodes]=N
    rows.append(f"| {nodes} | {nodes*32} GiB | {tot:.4e} | {N} | {N**3*BYTES/2**30:.1f} GiB |")
(D/"task10_memory_growth.md").write_text(f"""# Task 10 — Memory Ceiling vs. Weak Scaling

## Model
M(P) = c·P with c ≤ 32 GiB per node. Grid memory M = b·N³ with b bytes per cell.
**Assumption (parameterisable in `gen_calcs.py`):** b = 48 B/cell (6 double-precision field arrays). 1 GiB = 2³⁰ B.

Max cells per node: 32·2³⁰/48 = {cells_node:,} ≈ {cells_node:.3e}.
**N_max(P) = ⌊(P·32·2³⁰ / b)^(1/3)⌋**

| Nodes P | Aggregate memory | Max cells | N_max | Memory used at N_max |
|---:|---:|---:|---:|---:|
""" + "\n".join(rows) + f"""

## Interpretation
* 1 node: N ≈ {Ns[1]}. 64 nodes: N = {Ns[64]} (= 4× since 64^(1/3) = 4). 512 nodes: N = {Ns[512]} (= 8×).
* A 3D grid weak-scaled to fill memory grows linearly only as P^(1/3): 8× more nodes yields just 2× finer linear resolution. With a CFL limit (Δt ∝ Δx) work grows as P^(4/3), so memory-filling cannot hold wall-time constant (cf. Tasks 11, 13).
* Per-node memory stays at 32 GiB: the defining feature of memory-bounded scaling.
* If the application is not at the memory limit, Gustafson's fixed-time condition, not memory, decides N (Task 16).
""")

# ---- Task 16
N0=4096
rows="\n".join(f"| {p} | {N0*p**(1/3):.0f} | {p} | {(N0*p**(1/3))**2*8/p/2**20:.1f} MiB |" for p in [1,8,27,64,125,512,1000,4096])
(D/"task16_gemm_scaling.md").write_text(f"""# Task 16 — GEMM Dimension Scaling under Gustafson

## Proof
Work W(N) = 2N³ flops. Ideal per-processor time on P cores: T = 2N³/(P·r), r = per-core flop rate.
Fixed-time requirement T(P) = T(1) with baseline N₀: 2N³/(P r) = 2N₀³/r
⇒ N³ = P·N₀³ ⇒ **N(P) = N₀·P^(1/3)**. ∎

Consequences: total matrix memory ∝ N² ∝ P^(2/3) grows *slower* than P, so per-node memory shrinks as P^(−1/3): GEMM is never memory-limited under fixed-time scaling. Dimension grows ×2 for 8× processors, ×10 for 1000×.

Baseline N₀ = {N0}:

| P | N(P) | Work ratio W/W₀ | One N×N double matrix per processor |
|---:|---:|---:|---:|
{rows}

## Caveat
2D algorithms (SUMMA) move O(N²/√P) words per processor; with N ∝ P^(1/3) this scales as P^(2/3−1/2) = P^(1/6), so communication time slowly *grows* and α is not exactly constant (Task 12).
""")

# ---- Task 17
n=64
tab="\n".join(f"| {p} | {int(round(n*p**(1/3)))} | {n}³ | {6/n:.4f} | {6*p**(1/3)/(n*16**(1/3)) if False else 6*p**(1/3)/(n*round(1)) :.4f} |" for p in [1,8,64,512,4096])
(D/"task17_stencil_scaling.md").write_text(f"""# Task 17 — 3D 7-Point Stencil: Surface-to-Volume under Weak Scaling

## Setup
Global domain N³ on a P^(1/3)×P^(1/3)×P^(1/3) rank grid; each rank owns n³ cells, n = N/P^(1/3).
Compute per rank per step ∝ n³ (≈8 flops/cell); halo data = 6 faces × n² points.

**Communication/computation ratio per rank: ρ = 6n²/n³ = 6/n.**

## Weak scaling (volume ∝ P)
Fix n (work per rank constant ⇒ runtime constant ⇒ Gustafson fixed-time). Then N = n·P^(1/3) and **ρ = 6/n is independent of P**: it neither improves nor degrades. With n = {n}: ρ = {6/n:.4f}.
Strong scaling (fixed N₀ = {n}): n = N₀/P^(1/3) ⇒ ρ = 6P^(1/3)/N₀, growing as P^(1/3) — the Amdahl-style degradation (last column).

| P | Weak: N = n·P^(1/3) | Per-rank cells | ρ weak | ρ strong (N₀={n}) |
|---:|---:|---:|---:|---:|
""" + "\n".join(f"| {p} | {int(round(n*p**(1/3)))} | {n}³ | {6/n:.4f} | {6*p**(1/3)/n:.4f} |" for p in [1,8,64,512,4096]) + f"""

## α view
Per-rank halo time T_c = 6·t_s + t_w·6n² is independent of P (nearest-neighbour only) ⇒ α_comm = T_c/(T_c+T_comp) is constant ⇒ the stencil is a near-ideal Gustafson workload. Residual P-dependence: (i) global reductions (convergence/Δt): O(log P); (ii) network contention on non-ideal topologies; (iii) OS-noise amplification at barriers.

Proof of S/V: for a cube of side n, S/V = 6n²/n³ = 6/n, independent of P at fixed n. ∎
""")
print("ok", amax, sa, sg, Ns)
