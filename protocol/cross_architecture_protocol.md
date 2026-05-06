# Cross-Architecture Periodicity Protocol

Objective:
Test for invariant spectral peaks across architectures, regions, and kernels.

Procedure:
1. Collect 1,000,000 high-resolution timing deltas using perf_counter_ns().
2. Compute FFT spectrum.
3. Generate Monte Carlo baseline from Gaussian noise.
4. Compute z-score for maximum spectral amplitude.
5. Flag significance only if z-score > 10.

Reproducibility Rules:
- No manual seed control.
- No post-hoc frequency selection.
- No adaptive threshold adjustment.

Interpretation:
If no architecture yields z_score > 10, null hypothesis holds.
If one does, repeat 10 independent runs before interpretation.
If multiple independent architectures show same frequency peak above threshold,
initiate deep artifact audit before any theoretical claims.
