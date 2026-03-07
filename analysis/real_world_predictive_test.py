import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
import json
import sys

MIN_POINTS = 200

def persistence_model(history):
    return history[-1]

def ar1_forecast(history):
    if len(history) < 5:
        return history[-1]
    model = AutoReg(history, lags=1, old_names=False).fit()
    pred = model.predict(start=len(history), end=len(history))[0]
    return float(pred)

def hcm_forecast(history):
    alpha = 0.5087
    last = history[-1]
    return float(last*(1-alpha) + np.tanh(last)*alpha)

def rolling_test(series, forecast_func, train_ratio=0.7):

    split = int(len(series)*train_ratio)

    train = list(series[:split])
    test = series[split:]

    preds = []

    history = train.copy()

    for t in range(len(test)):

        pred = forecast_func(history)

        preds.append(pred)

        history.append(test[t])

    return mean_squared_error(test, preds)

def run(file_path):

    df = pd.read_csv(file_path)

    series = df.iloc[:,0].dropna().values.astype(float)

    if len(series) < MIN_POINTS:
        print("dataset too small")
        sys.exit(0)

    mse_persist = rolling_test(series, persistence_model)
    mse_ar = rolling_test(series, ar1_forecast)
    mse_hcm = rolling_test(series, hcm_forecast)

    result = {
        "persistence_mse": float(mse_persist),
        "ar1_mse": float(mse_ar),
        "hcm_mse": float(mse_hcm)
    }

    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    run(sys.argv[1])
