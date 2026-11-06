# Task 07 — Maximum Tolerable Serial Fraction

Given P = 8192, requirement S(P) ≥ 7500.

## Derivation
S(P) = P − α(P−1) ≥ S_min
⇒ α(P−1) ≤ P − S_min
⇒ **α_max = (P − S_min)/(P − 1)**   (valid since P > 1)

## Numbers
α_max = (8192 − 7500) / (8192 − 1) = 692 / 8191 = **0.084483** (≈ 8.448 %)

## Verification
S(8192) at α_max = 8192 − 0.084483·8191 = 7500.0000 ✓ (equals 7500).
Required efficiency: 7500/8192 = 0.9155.

## Remark
The bound is linear in α, so tolerance is generous: the serial phase may take up to ≈8.45 % of the *parallel-machine* wall-clock time.
For comparison, under Amdahl (uniprocessor-measured s) reaching S ≥ 7500 on 8192 cores would need s ≤ 1.126e-05 (≈0.0011 %), about 7500× stricter.
