# Task 05 — Historical Reconstruction: nCUBE/10 at Sandia (1988)

> Figures below are quoted from memory of the published paper (Gustafson, Montry & Benner, *Development of Parallel Methods for a 1024-Processor Hypercube*, SIAM J. Sci. Stat. Comput. 9(4), 1988) and of Gustafson's *Reevaluating Amdahl's Law* (CACM 31(5), 1988). **Verify exact values against the originals before citing.**

## Context
In 1985 Amdahl's law was widely cited to claim massively parallel machines could never exceed ~100× speedups — e.g. a 1 % serial fraction caps speedup at 100. Sandia researchers (Gustafson, Montry, Benner) built applications on a 1024-node nCUBE/10 hypercube (each node: 0.5 MB RAM, ~0.3 MFLOPS) and received the 1988 Karp Challenge and first Gordon Bell Prize for demonstrating speedups of **≈1000× on 1024 processors**.

## The three applications (as commonly reported)
Beam stress analysis (finite elements), baffled-surface wave motion (finite differences), and unstable fluid flow with a reaction-diffusion model (flux-corrected transport). Reported scaled speedups were about 1016–1021 on 1024 nodes; measured serial fractions on the parallel machine were small (< ~0.1–0.8 % of the parallel run time, depending on the program).

## Why Amdahl "forbade" it
With s = 0.4 %: S_A(1024) = 1/(0.004 + 0.996/1024) = 1/(0.004+0.000973) ≈ **201**; the ceiling 1/s = **250**. A measured ≈ 1000× is 4–5× beyond the bound.

## How problem expansion removed the ceiling
1. The experiment did not solve the same problem on every machine size. Each node held a fixed subdomain; the total grid grew with P (fixed-time scaling, ≈ 1024× more grid points).
2. The serial part (setup, I/O, broadcast) stayed ≈ constant in seconds, so on the parallel machine it was α ≈ 0.4–0.8 % of the run time.
3. Plugging α = 0.004 into the scaled law: S = 1024 − 0.004·1023 = **1019.9**, in line with the observed 1016–1021 (the match is the paper's point).
4. Memory was not a limit (grid ∝ aggregate memory ∝ P).
5. The same serial fraction, measured on the uniprocessor *with the small problem*, would be wrong for the large problem: s_scaled = α/(α+(1−α)P) ≈ 3.9·10⁻⁶ (Task 03).

## Lesson
The "ceiling" was an artefact of holding problem size fixed. Gustafson's reformulation (Task 02) showed that speedup of a *scaled* problem is linear with slope (1−α). Caveats: baseline T(1) could not be measured for the full problem (it did not fit one node's 0.5 MB); speedups were extrapolated/estimated from a scaled-down serial run, an inherent weakness of scaled-speedup reporting.
