# Gustafson's Law & Weak Scaling — Practice Repository

Parallel & Distributed Computing Architecture · Practice Task Sheet (Instructor: Sufyan bin Uzayr)

## Table of Contents
1. [Executive synthesis](#1-executive-synthesis)
2. [Core mathematical rules](#2-core-mathematical-rules)
3. [When to design around Gustafson weak scaling](#3-when-to-design-around-gustafson-weak-scaling)
4. [Execution commands](#4-execution-commands)
5. [Artifact index (Tasks 01–25)](#5-artifact-index)
6. [Honest limitations](#6-honest-limitations)

## 1. Executive synthesis
* Amdahl and Gustafson answer different questions: *fixed size, shrinking time* vs. *fixed time, growing size*. They are algebraically consistent: Gustafson = Amdahl applied to the scaled problem, whose uniprocessor serial fraction is α/(α+(1−α)P) → 0 (Task 03).
* Under Gustafson, efficiency tends to **1 − α**, not to 0 (Task 04); α = 4 % keeps E ≈ 96 % from 16 to 16 384 cores (Task 06).
* Reality departs from the law when (a) α or communication grows with P (Task 12), (b) work does not scale ∝ memory/P — superlinear algorithms, CG iteration growth, FFT all-to-all (Tasks 11, 13, 18), (c) memory caps problem growth (Task 10), (d) irregular workloads (Task 20).
* The isoefficiency of an ideal Gustafson program is Θ(P) — the best possible (Task 14). Embarrassingly parallel Monte Carlo (tree reductions, counter-based PRNG) and nearest-neighbour stencils (constant surface-to-volume at fixed local size) are the near-ideal cases (Tasks 17, 19).
* Weak scaling preserves energy per unit work up to the idle-power penalty during serial phases (Task 15).
* Empirical part: the harness, fitting and plotting pipeline are complete; the sandbox where it was run had **1 vCPU**, so the measured α ≈ 1.08 reflects oversubscription, not Gustafson behaviour (Task 24).

## 2. Core mathematical rules
| Rule | Formula |
|---|---|
| Scaled speedup | S(P) = P − α(P−1) = (1−α)P + α |
| Efficiency | E(P) = 1 − α(P−1)/P → 1 − α |
| Amdahl | S = 1/(s + (1−s)/P) ≤ 1/s ; E → 0 |
| Tolerable α for target S | α_max = (P − S)/(P − 1) |
| With communication | S_C = [P − α(P−1)]/(1 + C(P)) |
| Memory-bounded (Sun–Ni) | S = (s + pG(P))/(s + pG(P)/P) |
| Isoefficiency | W = K·T_o ; Gustafson program: T_o = α(P−1), W = Θ(P) |
| Effective α from data | α = (P − S)/(P − 1), or LS fit through origin of (P−S) vs (P−1) |

## 3. When to design around Gustafson weak scaling
Use it when the problem size is elastic (finer mesh, more particles/samples/ensemble members), per-rank work is local and linear in data size, serial parts are fixed in absolute time (I/O, setup) and collectives are logarithmic. Avoid relying on it when latency/deadline is fixed (use Amdahl/strong-scaling analysis), when complexity is superlinear or iterations grow with size, or when communication is all-to-all. Always report **both** weak- and strong-scaling results and the α measured *on the parallel run*.

## 4. Execution commands
```bash
pip install numpy matplotlib
python3 calculations/gen_calcs.py                 # regenerates Tasks 06-10, 16, 17
python3 benchmarks/simulator.py                   # Task 21: CSV + plots/simulator_overlay.{png,pdf}
python3 benchmarks/weak_scale_bench/weak_bench.py --threads 1 2 4 8 16 --runs 5 --k 10000000 --out benchmarks/results.csv   # Tasks 22-23
python3 benchmarks/fit_gustafson.py               # Task 23 regression -> fit_summary.csv, fit_result.json
python3 benchmarks/make_plots.py                  # Task 24 -> plots/scaling_comparison.{png,pdf}
```

## 5. Artifact index
| Task | Artifact |
|---|---|
| 01 | [theory/task01_scaling_models.md](theory/task01_scaling_models.md) |
| 02 | [theory/task02_derivation.md](theory/task02_derivation.md) |
| 03 | [theory/task03_serial_invariance.md](theory/task03_serial_invariance.md) |
| 04 | [theory/task04_asymptotic_limits.md](theory/task04_asymptotic_limits.md) |
| 05 | [theory/task05_historical_ncube.md](theory/task05_historical_ncube.md) |
| 06 | [calculations/task06_parametric_table.md](calculations/task06_parametric_table.md) |
| 07 | [calculations/task07_tolerable_serial.md](calculations/task07_tolerable_serial.md) |
| 08 | [calculations/task08_cross_divergence.md](calculations/task08_cross_divergence.md) |
| 09 | [calculations/task09_multicomponent.md](calculations/task09_multicomponent.md) |
| 10 | [calculations/task10_memory_growth.md](calculations/task10_memory_growth.md) |
| 11 | [theory/task11_sun_ni_comparison.md](theory/task11_sun_ni_comparison.md) |
| 12 | [theory/task12_communication_penalty.md](theory/task12_communication_penalty.md) |
| 13 | [theory/task13_failure_cases.md](theory/task13_failure_cases.md) |
| 14 | [theory/task14_isoefficiency.md](theory/task14_isoefficiency.md) |
| 15 | [theory/task15_energy_scaling.md](theory/task15_energy_scaling.md) |
| 16 | [calculations/task16_gemm_scaling.md](calculations/task16_gemm_scaling.md) |
| 17 | [calculations/task17_stencil_scaling.md](calculations/task17_stencil_scaling.md) |
| 18 | [analysis/task18_nbody_scaling.md](analysis/task18_nbody_scaling.md) |
| 19 | [analysis/task19_monte_carlo.md](analysis/task19_monte_carlo.md) |
| 20 | [analysis/task20_graph_processing.md](analysis/task20_graph_processing.md) |
| 21 | [benchmarks/simulator.py](benchmarks/simulator.py), `benchmarks/simulator_output.csv`, `plots/simulator_overlay.*` |
| 22 | [benchmarks/weak_scale_bench/](benchmarks/weak_scale_bench/) |
| 23 | `benchmarks/results.csv`, [benchmarks/fit_gustafson.py](benchmarks/fit_gustafson.py), `benchmarks/fit_summary.csv` |
| 24 | `plots/scaling_comparison.{png,pdf}`, [analysis/task24_hardware_audit.md](analysis/task24_hardware_audit.md) |
| 25 | this README |

## 6. Honest limitations
* Task 05 figures are quoted from memory — verify against the original papers.
* Task 10 assumes 48 B per grid cell (stated, adjustable); Task 09 treats phase B as serial per the task wording.
* Empirical data (Tasks 22–24) come from a 1-vCPU VM; re-run on multi-core hardware and update `analysis/task24_hardware_audit.md` with your machine's `lscpu`/`numactl -H`.
