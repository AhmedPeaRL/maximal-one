import numpy as np
import pandas as pd
import json
from pathlib import Path

ART = Path("artifacts")

# -----------------------------
# Load series
# -----------------------------

def load_series():
    path = Path("real-data/sunspots_global_prepared.csv")
    if not path.exists():
        return None

    df = pd.read_csv(path)
    return df.values.squeeze()


# -----------------------------
# HARD transformations
# -----------------------------

def difference(series):
    return np.diff(series)


def shuffled_blocks(series, block_size=20):
    blocks = [
        series[i:i+block_size]
        for i in range(0, len(series), block_size)
    ]
    np.random.shuffle(blocks)
    return np.concatenate(blocks)


def noise_injection(series, noise_level=0.2):
    noise = np.random.normal(0, noise_level*np.std(series), size=len(series))
    return series + noise

def phase_scramble(series):
    fft = np.fft.rfft(series)
    phases = np.angle(fft)
    magnitudes = np.abs(fft)

    random_phases = np.random.uniform(-np.pi, np.pi, size=len(phases))
    scrambled = magnitudes * np.exp(1j * random_phases)

    return np.fft.irfft(scrambled, n=len(series))


# -----------------------------
# predictors
# -----------------------------

def persistence(history):
    return history[-1]

def hcm_predict(history):
    window = 20

    if len(history) < window:
        return history[-1]

    series = np.array(history[-window:])

    # normalize
    series = (series - np.mean(series)) / (np.std(series) + 1e-8)

    # --- Takens embedding (light) ---
    tau = 2
    dim = 3

    embedded = []
    for i in range(len(series) - tau * dim):
        point = [series[i + j * tau] for j in range(dim)]
        embedded.append(point)

    embedded = np.array(embedded)

    if len(embedded) < 5:
        return history[-1]

    current = embedded[-1]

    # --- nearest neighbors ---
    dists = np.linalg.norm(embedded - current, axis=1)
    idx = np.argsort(dists)[1:4]

    future = []

    for i in idx:
        if i + 1 < len(embedded):
            future.append(embedded[i + 1][-1])

    if len(future) == 0:
        return history[-1]

    # --- evolve state ---
    prediction = np.mean(future)

    # denormalize
    prediction = prediction * np.std(history[-window:]) + np.mean(history[-window:])

    return float(prediction)
    
# -----------------------------
# evaluation
# -----------------------------

def rolling_mse(series, model):

    split = int(len(series)*0.7)
    train = list(series[:split])
    test = series[split:]

    history = train.copy()
    preds = []

    for t in range(len(test)):
        preds.append(model(history))
        history.append(test[t])

    return float(np.mean((np.array(test) - np.array(preds))**2))


# -----------------------------
# core
# -----------------------------

def evaluate(series):

    tests = {}

    # original
    tests["original"] = series

    # diff
    tests["diff"] = difference(series)

    # shuffled
    tests["shuffled"] = shuffled_blocks(series)

    # noisy
    tests["noisy"] = noise_injection(series)
 
    # scramble
    tests["phase"] = phase_scramble(series)

    results = {}

    for name, s in tests.items():

        if len(s) < 100:
            continue

        mse_p = rolling_mse(s, persistence)
        mse_h = rolling_mse(s, hcm_predict)

        results[name] = {
            "persistence_mse": mse_p,
            "hcm_mse": mse_h,
            "hcm_better": mse_h < mse_p
        }

    return results


def main():

    series = load_series()

    if series is None:
        result = {"skipped": True}
    else:
        result = evaluate(series)

        # pass condition: HCM wins in at least 2 hard regimes
        wins = sum(1 for r in result.values() if r["hcm_better"])

        result["hard_non_trivial"] = (
            wins >= 2 and 
            result.get("diff", {}).get("hcm_better", False)
        )

    ART.mkdir(exist_ok=True)
    (ART / "anti_triviality_hard.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
