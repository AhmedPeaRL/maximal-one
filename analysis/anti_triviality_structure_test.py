import numpy as np
import json
from pathlib import Path

from analysis.hcm_meta_predictor import HCMMetaPredictor

ART = Path("artifacts")
ART.mkdir(exist_ok=True)


def to_native(obj):
    """
    🔥 Convert numpy types to pure Python types for JSON safety
    """
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, dict):
        return {k: to_native(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_native(v) for v in obj]
    return obj


def generate_structured_series(n=300):
    t = np.arange(n)

    # nonlinear + multi-scale + chaos mix
    series = (
        np.sin(2*np.pi*t/11)
        + 0.5*np.sin(2*np.pi*t/3)
        + 0.3*np.sin(2*np.pi*t/50)
    )

    # nonlinear distortion
    series = np.tanh(series) + 0.1 * np.random.randn(n)

    return series


def destroy_local_predictability(series):
    noise = np.random.normal(0, 0.3, size=len(series))
    return series + noise


def evaluate(series, model):
    split = int(len(series)*0.7)
    train = list(series[:split])
    test = series[split:]

    history = train.copy()
    preds = []

    for t in range(len(test)):
        p = model.predict(history)
        preds.append(p)
        history.append(test[t])

    return np.mean((np.array(test) - np.array(preds))**2)


def main():
    np.random.seed(42)

    base_series = generate_structured_series()
    corrupted = destroy_local_predictability(base_series)

    model = HCMMetaPredictor()

    mse_clean = evaluate(base_series, model)
    mse_corrupt = evaluate(corrupted, model)

    result = {
        "clean_mse": mse_clean,
        "corrupted_mse": mse_corrupt,
        "structure_detected": mse_clean < mse_corrupt
    }

    # 🔥 تحويل آمن قبل الطباعة والحفظ
    result = to_native(result)

    print("=== STRUCTURE TEST ===")
    print(json.dumps(result, indent=2))

    (ART / "anti_triviality_structure.json").write_text(
        json.dumps(result, indent=2)
    )


if __name__ == "__main__":
    main()
