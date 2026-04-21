import numpy as np

def estimate_alpha(series):
    """
    Robust spectral alpha estimation
    """

    # Remove mean
    series = series - np.mean(series)

    n = len(series)

    # Apply window (reduces leakage)
    window = np.hanning(n)
    series = series * window

    # FFT
    fft_vals = np.fft.rfft(series)
    psd = (np.abs(fft_vals) ** 2) / n

    freqs = np.fft.rfftfreq(n)

    # Remove zero freq
    mask = freqs > 0
    freqs = freqs[mask]
    psd = psd[mask]

    # Log binning (critical fix)
    num_bins = 20
    log_bins = np.logspace(np.log10(freqs.min()), np.log10(freqs.max()), num_bins)

    binned_freqs = []
    binned_psd = []

    for i in range(len(log_bins)-1):
        idx = (freqs >= log_bins[i]) & (freqs < log_bins[i+1])
        if np.sum(idx) > 0:
            binned_freqs.append(np.mean(freqs[idx]))
            binned_psd.append(np.mean(psd[idx]))

    binned_freqs = np.array(binned_freqs)
    binned_psd = np.array(binned_psd)

    # Remove extreme edges
    trim = int(0.1 * len(binned_freqs))
    if trim > 0:
        binned_freqs = binned_freqs[trim:-trim]
        binned_psd = binned_psd[trim:-trim]

    # Log-log fit
    log_f = np.log(binned_freqs)
    log_psd = np.log(binned_psd + 1e-12)

    slope, _ = np.polyfit(log_f, log_psd, 1)

    alpha = -slope

    return float(alpha)
