import numpy as np
from math import log
from sympy import divisor_count
import matplotlib.pyplot as plt

N = 5000

tau = np.array([divisor_count(n) for n in range(1, N+1)])
delta = tau - np.log(np.arange(1, N+1))

# Fourier Transform
fft_vals = np.fft.fft(delta)
power_spectrum = np.abs(fft_vals)**2

plt.figure()
plt.plot(power_spectrum[:200])
plt.title("Power Spectrum of Δ(n)")
plt.show()
