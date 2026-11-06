#!/usr/bin/env python3
"""Task 21 - Amdahl vs Gustafson simulator.
Usage: python3 simulator.py [--alphas 0.001 0.01 0.05 0.2] [--pmax 65536] [--out-dir .] [--plots-dir ../plots]
Writes simulator_output.csv (P, alpha, amdahl_speedup, gustafson_speedup, amdahl_eff, gustafson_eff)
and overlay plots (strong vs weak scaling)."""
import argparse, csv, os
import numpy as np

def amdahl(P, s):    return 1.0 / (s + (1.0 - s) / P)
def gustafson(P, a): return P - a * (P - 1.0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--alphas", type=float, nargs="+", default=[0.001, 0.01, 0.04, 0.08, 0.20])
    ap.add_argument("--pmax", type=int, default=65536)
    ap.add_argument("--out-dir", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--plots-dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plots"))
    ap.add_argument("--no-plots", action="store_true")
    a = ap.parse_args()
    if not 1 <= a.pmax <= 65536: ap.error("pmax must be in [1, 65536]")
    for x in a.alphas:
        if not 0.001 <= x <= 0.20: ap.error(f"alpha {x} outside [0.001, 0.20]")
    Ps = np.unique(np.concatenate([2 ** np.arange(0, int(np.log2(a.pmax)) + 1), [a.pmax]])).astype(float)
    os.makedirs(a.out_dir, exist_ok=True)
    path = os.path.join(a.out_dir, "simulator_output.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["P", "alpha", "amdahl_speedup", "gustafson_speedup", "amdahl_efficiency", "gustafson_efficiency"])
        for al in a.alphas:
            for P in Ps:
                sa, sg = amdahl(P, al), gustafson(P, al)
                w.writerow([int(P), al, f"{sa:.6f}", f"{sg:.6f}", f"{sa/P:.8f}", f"{sg/P:.8f}"])
    print("wrote", path)
    if a.no_plots: return
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    os.makedirs(a.plots_dir, exist_ok=True)
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    cols = plt.cm.viridis(np.linspace(0, 0.9, len(a.alphas)))
    for c, al in zip(cols, a.alphas):
        ax[0].loglog(Ps, amdahl(Ps, al), "--", color=c, label=f"Amdahl s={al}")
        ax[0].loglog(Ps, gustafson(Ps, al), "-", color=c, label=f"Gustafson α={al}")
        ax[1].semilogx(Ps, amdahl(Ps, al) / Ps, "--", color=c)
        ax[1].semilogx(Ps, gustafson(Ps, al) / Ps, "-", color=c)
    ax[0].loglog(Ps, Ps, "k:", label="Ideal S=P")
    ax[0].set(xlabel="P (cores)", ylabel="Speedup", title="Strong (Amdahl, dashed) vs weak (Gustafson, solid)")
    ax[0].legend(fontsize=6, ncol=2); ax[0].grid(True, which="both", alpha=.3)
    ax[1].set(xlabel="P (cores)", ylabel="Efficiency S/P", title="Parallel efficiency", ylim=(0, 1.02))
    ax[1].grid(True, which="both", alpha=.3)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(a.plots_dir, f"simulator_overlay.{ext}"), dpi=200)
    print("wrote plots to", a.plots_dir)

if __name__ == "__main__":
    main()
