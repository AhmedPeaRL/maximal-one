import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
import json
import sys

np.random.seed(42)

def rolling_forecast(model_func, series, train_ratio=0.7):
    n = len(series)
    split = int(n * train_ratio)

    train = series[:split]
    test = series[split:]

    preds = []
    history = list(train)

    for t in range(len(test)):
        model = model_func(np.array(history))
        yhat = model(history[-1])
        preds.append(yhat)
        history.append(test[t])

    return mean_squared_error(test, preds)

def ar1_model(history):
    model = AutoReg(history, lags=1, old_names=False).fit()
    return lambda last: model.predict(start=len(history), end=len(history))[0]

def hcm_recursive(history):
    alpha = 0.5087
    return lambda last: last * (1 - alpha) + np.tanh(last) * alpha

def run(file_path):
    df = pd.read_csv(file_path)
    series = df.iloc[:,0].dropna().values

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
