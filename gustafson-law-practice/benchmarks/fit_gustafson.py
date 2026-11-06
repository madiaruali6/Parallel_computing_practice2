#!/usr/bin/env python3
"""Task 23 - mean/std per config + least-squares fit of alpha to S(P)=P-alpha(P-1).
Scaled speedup per run: S_i(P) = P * mean(T(1)) / T_i(P)   (work grows by P at constant per-worker K).
Fit (through the origin in y = P - S, x = P-1):  alpha = sum(x*y)/sum(x*x).
Writes fit_summary.csv and fit_result.json next to results.csv."""
import csv, json, os, sys, math
from collections import defaultdict
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "results.csv")
T = defaultdict(list); hw = 1
for r in csv.DictReader(open(src)):
    T[int(r["threads"])].append(float(r["wall_seconds"])); hw = int(r["hw_concurrency"])
Ps = sorted(T)
assert 1 in Ps and len(Ps) >= 5, "need P=1 and >=5 thread counts"
t1 = np.mean(T[1])
rows = []
for P in Ps:
    t = np.array(T[P]); n = len(t)
    S = P * t1 / t
    rows.append(dict(P=P, n=n, mean_s=t.mean(), std_s=t.std(ddof=1), S_mean=S.mean(),
                     S_se=S.std(ddof=1) / math.sqrt(n), E=S.mean() / P))
x = np.array([r["P"] - 1 for r in rows], float); y = np.array([r["P"] - r["S_mean"] for r in rows])
alpha = float((x * y).sum() / (x * x).sum())
resid = y - alpha * x
se_alpha = float(math.sqrt((resid ** 2).sum() / (len(x) - 1) / (x * x).sum())) if len(x) > 1 else float("nan")
with open(os.path.join(here, "fit_summary.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
json.dump(dict(alpha_observed=alpha, alpha_stderr=se_alpha, hw_concurrency=hw, t1_mean=t1), open(os.path.join(here, "fit_result.json"), "w"), indent=2)
print(f"{'P':>3} {'mean(s)':>9} {'std(s)':>8} {'S':>7} {'SE(S)':>7} {'E':>6}")
for r in rows: print(f"{r['P']:>3} {r['mean_s']:9.4f} {r['std_s']:8.4f} {r['S_mean']:7.3f} {r['S_se']:7.3f} {r['E']:6.3f}")
print(f"alpha_observed = {alpha:.4f} +/- {se_alpha:.4f}  (hw concurrency = {hw})")
if alpha > 1 or alpha < 0:
    print("NOTE: alpha outside [0,1] -> model assumptions violated (e.g. P > physical cores: oversubscription).")
