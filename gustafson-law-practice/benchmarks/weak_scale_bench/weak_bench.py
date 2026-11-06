#!/usr/bin/env python3
"""Task 22 - weak-scaling harness (Python multiprocessing).
Workload: midpoint-rule integration of f(x)=4/(1+x^2) over [0,1] (=pi).
Weak scaling: every worker integrates K points (constant per worker) -> total work = P*K.
A deliberately small serial section (setup + final reduction) is timed inside the wall-clock.
Usage: python3 weak_bench.py --threads 1 2 4 8 --runs 5 --k 20000000 --out ../results.csv
Wall time per run = process-pool launch excluded? NO: pool creation IS included to expose real serial cost."""
import argparse, csv, math, multiprocessing as mp, os, time
import numpy as np

CHUNK = 2_000_000

def integrate(args):
    lo, n, total = args           # integrate indices [lo, lo+n) of `total` midpoints
    h = 1.0 / total; acc = 0.0
    for s in range(lo, lo + n, CHUNK):
        m = min(CHUNK, lo + n - s)
        x = (np.arange(s, s + m, dtype=np.float64) + 0.5) * h
        acc += float(np.sum(4.0 / (1.0 + x * x)))
    return acc * h

def run_once(P, K):
    total = P * K
    t0 = time.perf_counter()
    jobs = [(i * K, K, total) for i in range(P)]
    if P == 1:
        parts = [integrate(jobs[0])]
    else:
        with mp.get_context("fork").Pool(P) as pool:
            parts = pool.map(integrate, jobs, chunksize=1)
    pi = math.fsum(parts)         # serial reduction
    t = time.perf_counter() - t0
    assert abs(pi - math.pi) < 1e-6, pi
    return t

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threads", type=int, nargs="+", default=None)
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--k", type=int, default=20_000_000, help="points per worker (constant)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results.csv"))
    a = ap.parse_args()
    hw = os.cpu_count() or 1
    if a.threads is None:
        a.threads = sorted({1, 2, 4, 8, hw} | {max(1, hw // 2)}) if hw > 1 else [1, 2, 3, 4, 6]
    run_once(1, 100000)           # warm-up
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["threads", "run", "k_per_worker", "wall_seconds", "hw_concurrency"])
        for P in a.threads:
            for r in range(a.runs):
                t = run_once(P, a.k)
                w.writerow([P, r, a.k, f"{t:.6f}", hw]); f.flush()
                print(f"P={P:3d} run={r} t={t:.3f}s", flush=True)
    print("wrote", a.out)

if __name__ == "__main__":
    main()
