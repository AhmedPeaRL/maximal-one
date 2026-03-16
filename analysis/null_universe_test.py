import numpy as np
import json
from pathlib import Path

OUT = "artifacts/null_universe_test.json"


def spectral_alpha(x):

    x = x - np.mean(x)

    f = np.fft.rfft(x)
    psd = np.abs(f)**2

    freqs = np.fft.rfftfreq(len(x))

    mask = freqs > 0

    freqs = freqs[mask]
    psd = psd[mask]

    logf = np.log(freqs)
    logp = np.log(psd)

    slope = np.polyfit(logf, logp,1)[0]

    return -slope


def generate_white(n):

    return np.random.normal(0,1,n)


def generate_brown(n):

    return np.cumsum(np.random.normal(0,1,n))


def generate_random_walk(n):

    return np.cumsum(np.random.choice([-1,1],n))


def run():

    np.random.seed(42)

    N = 2000

    universe = {
        "white_noise": spectral_alpha(generate_white(N)),
        "brown_noise": spectral_alpha(generate_brown(N)),
        "random_walk": spectral_alpha(generate_random_walk(N))
    }

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUT,"w") as f:
        json.dump(universe,f,indent=2)

    print(json.dumps(universe,indent=2))


if __name__ == "__main__":
    run()
