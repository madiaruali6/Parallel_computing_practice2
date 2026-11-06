# Task 24 — Hardware Audit and Empirical-vs-Theoretical Discrepancy

## Hardware used (sandbox container, `lscpu` raw output in `analysis/lscpu_raw.txt`)
| Item | Value |
|---|---|
| CPU | Intel Xeon (family 6, model 207 → Sapphire Rapids class) @ 2.10 GHz, KVM guest |
| Visible hardware threads | **1** (1 socket × 1 core × 1 thread) |
| Caches reported | L1d 48 KiB, L1i 32 KiB, L2 2 MiB, L3 260 MiB (shared host LLC, as visible to the VM) |
| NUMA | 1 node |
| RAM | ≈3 GiB visible |
| Memory channels | not exposed by the hypervisor (cannot be audited from inside the VM) |
| Vector ISA | AVX2, AVX-512 (NumPy used) |
| Turbo/DVFS/thermal | not observable inside the VM |

> **Replace this table with your own machine** (`lscpu`, `numactl -H`, `lstopo`) before submitting if you re-run the suite on real hardware.

## Result (see `plots/scaling_comparison.{png,pdf}`, `benchmarks/fit_summary.csv`)
Measured with P = 1, 2, 3, 4, 6, 8 workers, 5 runs each, 10⁷ points/worker:

| P | mean T (s) | S(P) | E |
|---:|---:|---:|---:|
| 1 | 0.050 | 1.03 | 1.03 |
| 2 | 0.160 | 0.63 | 0.32 |
| 3 | 0.268 | 0.57 | 0.19 |
| 4 | 0.325 | 0.62 | 0.15 |
| 6 | 0.484 | 0.62 | 0.10 |
| 8 | 0.690 | 0.58 | 0.07 |

Fitted **α_observed = 1.08 ± 0.02** — outside the physical range [0,1].

## Interpretation (honest)
* The VM has **one** vCPU. All P worker processes time-share it, so wall time grows ≈ ∝ P (T(8)/T(1) ≈ 14). This is *oversubscription*, not weak scaling: the measurement validates that the harness correctly reports "no parallel hardware ⇒ S ≈ 0.6", and it **does not measure Gustafson's law**.
* S < 1 arises because pool creation/fork, IPC pickling and context switching are added to the serial cost; α > 1 is the regression's way of saying "worse than serial". The first P=1 run included a warm-up effect (T(1) std 22 %), so S(1) = 1.03 rather than exactly 1.
* **NUMA/thermal effects could not be observed** (1 node, no frequency telemetry). On real hardware expect: (a) thermal/power throttling and turbo-bin reduction as more cores are active (all-core clock < single-core clock) — lowers S below linear even with α = 0; (b) NUMA: first-touch placement and cross-socket traffic penalise P beyond one socket's cores; our kernel streams 16 MB NumPy temporaries per chunk (2·10⁶ doubles), larger than a typical L2, so it is sensitive to memory-channel bandwidth; (c) SMT: P > physical cores shares execution units, giving ≤ 1.2–1.3× instead of 2×; (d) fork + pool-start cost is part of α (≈10–20 ms here).
* Re-run with `python3 benchmarks/weak_scale_bench/weak_bench.py` on a multi-core host; no code changes needed.

## Plot content
(1) ideal S = P (dotted), (2) Gustafson fit (blue), (3) measured ± SE (green), (4) Amdahl with the same s (red; undefined for s ≥ 1, so shown only in legend for this dataset). For a well-behaved dataset use `simulator_overlay.png` to see the expected shapes.

---
## UPDATE: measurement on the author's machine (supersedes the sandbox section above)

Hardware: Apple M4, 10 logical CPUs, 16 GiB RAM, macOS 26.7.1. Fanless MacBook Air (thermal throttling possible). Apple Silicon has heterogeneous performance/efficiency cores.

Weak-scaling run: P = 1, 2, 4, 6, 8, 10 workers, 5 runs each, 5·10^8 points per worker.

| P | mean T (s) | S(P) | E(P) |
|---:|---:|---:|---:|
| 1 | 0.553 | 1.00 | 1.00 |
| 2 | 0.961 | 1.15 | 0.58 |
| 4 | 1.863 | 1.19 | 0.30 |
| 6 | 2.876 | 1.15 | 0.19 |
| 8 | 3.949 | 1.12 | 0.14 |
| 10 | 4.969 | 1.11 | 0.11 |

Fitted alpha_observed = 0.98 +/- 0.01.

Interpretation: runtime grows almost proportionally to P, so the scaled speedup saturates near 1.1-1.2 instead of following S = P - alpha(P-1) with small alpha. Gustafson's premise (constant per-worker time) is violated, so the large fitted alpha is an *effective* value that lumps together every non-scaling effect, not a measure of serial code. Likely cause (hypothesis, not verified by a second experiment): the kernel streams 16 MB NumPy temporaries per chunk, larger than L2, so it is limited by shared DRAM bandwidth, which a single core already largely saturates; extra workers add no throughput. Other contributing factors: efficiency cores being slower than performance cores, fanless thermal throttling, and process start-up cost (fork) included in the timing. NUMA is not applicable (single memory domain on Apple Silicon). A first run with 10^7 points/worker was dominated by process start-up (~10 ms per worker) and gave alpha ~ 1.0 as well.

Follow-up (not done): shrink the working set to fit in cache (weak_bench.py was updated for this in a later revision) and re-measure; if S then rises, the memory-bandwidth explanation is confirmed.
