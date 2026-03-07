import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
import json
import sys

np.random.seed(42)

MIN_HISTORY = 10
MIN_POINTS = 300


def safe_exit(reason):
    result = {
        "hcm_superior": False,
        "skipped": True,
        "reason": reason
    }
    print(json.dumps(result))
    sys.exit(0)


def rolling_forecast(model_func, series, train_ratio=0.7):

    n = len(series)

    if n < MIN_HISTORY * 2:
        safe_exit("series_too_short")

    split = int(n * train_ratio)

    train = series[:split]
    test = series[split:]

    preds = []
    history = list(train)

    for t in range(len(test)):

        if len(history) < MIN_HISTORY:
            preds.append(history[-1])
            history.append(test[t])
            continue

        try:
            model = model_func(np.array(history))
            yhat = model(history[-1])
        except Exception:
            yhat = history[-1]

        preds.append(float(yhat))
        history.append(test[t])

    return mean_squared_error(test, preds)


def ar1_model(history):

    if len(history) < MIN_HISTORY:
        return lambda last: last

    model = AutoReg(history, lags=1, old_names=False).fit()

    return lambda last: float(
        model.predict(start=len(history), end=len(history))[0]
    )


def hcm_recursive(history):

    alpha = 0.5087

    return lambda last: float(
        last * (1 - alpha) + np.tanh(last) * alpha
    )


def run(file_path):

    df = pd.read_csv(file_path)

    series = df.iloc[:, 0].dropna().values.astype(float)

    if len(series) < MIN_POINTS:
        safe_exit("dataset_too_small")

    ar_mse = rolling_forecast(ar1_model, series)
    hcm_mse = rolling_forecast(hcm_recursive, series)

    delta = ar_mse - hcm_mse

    result = {
        "ar_mse": float(ar_mse),
        "hcm_mse": float(hcm_mse),
        "delta_mse": float(delta),
        "hcm_superior": bool(delta > 0)
    }

    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    run(sys.argv[1])
