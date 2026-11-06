# Task 01 — Strong vs. Weak Scaling: Amdahl (1967) and Gustafson (1988)

## 1. Core assumptions
| | Amdahl (1967) | Gustafson–Barsis (1988) |
|---|---|---|
| Question asked | How much faster can I solve *this* problem? | How large a problem can I solve in *this* time? |
| Held fixed | Total workload W | Wall-clock runtime T |
| Varied | Time (shrinks) | Workload (grows) |
| Serial fraction | s of the 1-core run time | α of the P-core run time |
| Scaling type | Strong scaling, fixed-size | Weak scaling, fixed-time |
| Formula | S = 1/(s + (1−s)/P) | S = P − α(P−1) |

## 2. Behaviour of problem size as P → ∞
* **Amdahl:** N(P) = N₀ for all P. Per-processor work W/P → 0, the serial time s·T₁ is untouched, so it eventually dominates: S → 1/s (e.g. s = 0.05 ⇒ S ≤ 20 however many cores).
* **Gustafson:** N(P) grows (W(P) = s + pP in units of T) so that per-processor work stays constant. The parallel part grows linearly in P, the serial part is constant in absolute time, so its *relative* weight in the equivalent serial workload vanishes: S(P) ∼ (1−α)P → ∞.

## 3. Why "fixed-size" vs. "fixed-time"
Amdahl's law keeps the **size** of the input constant and lets time vary; Gustafson's keeps the **time** constant (the user's patience/deadline, e.g. overnight forecast) and lets the size vary. The terms describe the invariant of the thought experiment, not a property of the hardware.

## 4. Philosophical / physical divergence
Amdahl treats the program as a *given*; parallelism is a tool to shorten an existing job, and the law is therefore a pessimistic bound on the benefit of adding processors. Gustafson treats the *machine* as the given resource: users buy bigger machines to attack bigger problems (finer meshes, more particles), so the parallel part of the work expands while the serial part (setup, I/O of fixed size, control logic) does not. Physically, that is what happens in practice in scientific computing: resolution and accuracy requirements grow with available compute. Neither law is wrong; they answer different questions and are special cases of the memory-bounded model of Sun & Ni (Task 11): G(P) = 1 gives Amdahl and G(P) = P gives Gustafson.

## 5. Practical consequence
Use Amdahl for *latency-critical* workloads with fixed inputs (real-time inference, a fixed query). Use Gustafson for *throughput/capability* workloads whose size is elastic (simulation, rendering, Monte Carlo).
