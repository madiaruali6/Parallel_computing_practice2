#!/usr/bin/env python3
"""Task 24 - publication plots: ideal, Gustafson(fit), measured +/- SE, Amdahl(same alpha)."""
import csv, json, os
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "..", "plots"); os.makedirs(out, exist_ok=True)
rows = list(csv.DictReader(open(os.path.join(here, "fit_summary.csv"))))
fit = json.load(open(os.path.join(here, "fit_result.json")))
P = np.array([int(r["P"]) for r in rows], float); S = np.array([float(r["S_mean"]) for r in rows]); se = np.array([float(r["S_se"]) for r in rows])
a = fit["alpha_observed"]; Pf = np.linspace(1, P.max() * 1.05, 200)
plt.rcParams.update({"font.size": 10, "font.family": "serif"})
fig, ax = plt.subplots(figsize=(6.5, 4.6))
ax.plot(Pf, Pf, "k:", label="Ideal linear S = P")
ax.plot(Pf, Pf - a * (Pf - 1), "-", color="tab:blue", label=f"Gustafson fit (α = {a:.3f})")
if 0 <= a < 1:
    ax.plot(Pf, 1 / (a + (1 - a) / Pf), "--", color="tab:red", label=f"Amdahl, same s = {a:.3f}")
else:
    ax.plot([], [], "--", color="tab:red", label="Amdahl: undefined for s ∉ [0,1)")
ax.errorbar(P, S, yerr=se, fmt="o", color="tab:green", capsize=3, label="Measured (mean ± SE, n=5)")
ax.set(xlabel="Workers P (weak scaling, constant work per worker)", ylabel="Scaled speedup S(P) = P·T(1)/T(P)",
       title=f"Weak-scaling measurement ({fit['hw_concurrency']} hardware thread(s))")
ax.set_ylim(bottom=min(0, S.min() - 1)); ax.grid(alpha=.3); ax.legend(fontsize=8)
fig.tight_layout()
for ext in ("png", "pdf"): fig.savefig(os.path.join(out, f"scaling_comparison.{ext}"), dpi=300)
print("saved plots/scaling_comparison.{png,pdf}")
