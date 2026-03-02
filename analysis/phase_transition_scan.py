import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)

def simulate_system(gamma, n=4096):
    x = np.zeros(n)
    noise = np.random.normal(0,1,n)

    for t in range(1,n):
        x[t] = gamma * x[t-1] + noise[t]

    return x

def estimate_alpha(signal):
    freqs = np.fft.rfftfreq(len(signal))
    psd = np.abs(np.fft.rfft(signal))**2

    freqs = freqs[1:]
    psd = psd[1:]

    slope, _, _, _, _ = stats.linregress(np.log(freqs), np.log(psd))
    return -slope

gammas = np.linspace(0.1, 0.99, 40)
alphas = []

for g in gammas:
    sig = simulate_system(g)
    alpha = estimate_alpha(sig)
    alphas.append(alpha)

alphas = np.array(alphas)

# Detect curvature (second derivative)
curvature = np.gradient(np.gradient(alphas))

critical_index = np.argmax(np.abs(curvature))
gamma_c = gammas[critical_index]

print("=== Phase Scan Results ===")
print("Critical gamma candidate:", gamma_c)
print("Alpha at critical:", alphas[critical_index])

plt.plot(gammas, alphas)
plt.axvline(gamma_c, linestyle='--')
plt.xlabel("gamma")
plt.ylabel("alpha")
plt.title("Phase Transition Scan")
plt.savefig("artifacts/phase_transition.png")
