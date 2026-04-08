import json
import requests
import hashlib
import pandas as pd
import numpy as np

OUTPUT_PATH = "artifacts/external_validation.json"


def fetch_external_dataset():
    """
    Pull real-world dataset (independent of repo)
    """
    url = "https://raw.githubusercontent.com/datasets/global-temp/master/data/monthly.csv"
    
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return None


def compute_signature(df):
    """
    Extract invariant-like statistical signature
    """
    values = df.iloc[:, -1].dropna().values
    
    mean = float(np.mean(values))
    std = float(np.std(values))
    
    spectrum = np.fft.fft(values)
    power = float(np.mean(np.abs(spectrum)))
    
    return {
        "mean": mean,
        "std": std,
        "spectral_power": power
    }


def build_external_proof(signature):
    raw = json.dumps(signature, sort_keys=True)
    h = hashlib.sha256(raw.encode()).hexdigest()
    
    return {
        "signature": signature,
        "hash": h
    }


def main():
    df = fetch_external_dataset()
    
    if df is None:
        result = {
            "status": "failed_fetch"
        }
    else:
        sig = compute_signature(df)
        proof = build_external_proof(sig)
        
        result = {
            "status": "ok",
            "proof": proof
        }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
