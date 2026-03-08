import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from analysis.lyapunov_neural_predictor import LyapunovNeuralPredictor
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

    model = model_func()
    model.fit(train)

    preds = []
    history = list(train)

    for t in range(len(test)):

        if len(history) < MIN_HISTORY:
            pred = history[-1]

        else:
            pred = model.predict(history)

            # ضمان أن القيمة رقم واحد فقط
            if isinstance(pred, (list, np.ndarray)):
                pred = float(np.asarray(pred).squeeze())

        preds.append(float(pred))

        history.append(test[t])

    return np.array(test), np.array(preds)


def compute_mse(model_func, series):

    test, preds = rolling_forecast(model_func, series)

    return mean_squared_error(test, preds)


def ar1_model():

    class ARWrapper:

        def fit(self, history):
            if len(history) < MIN_HISTORY:
                self.model = None
                return

            self.model = AutoReg(history, lags=1, old_names=False).fit()

        def predict(self, history):

            if self.model is None:
                return history[-1]

            return float(
                self.model.predict(start=len(history), end=len(history))[0]
            )

    return ARWrapper()


def hcm_recursive():

    class HCMModel:

        def fit(self, history):
            self.alpha = 0.5087

        def predict(self, history):
            last = history[-1]
            return float(last * (1 - self.alpha) + np.tanh(last) * self.alpha)

    return HCMModel()


def run(file_path):

    df = pd.read_csv(file_path)

    series = df.values.squeeze()

    if len(series) < MIN_POINTS:
        safe_exit("dataset_too_small")

    mse = compute_mse(LyapunovNeuralPredictor, series)

    ar_mse = compute_mse(ar1_model, series)

    hcm_mse = compute_mse(hcm_recursive, series)

    delta = ar_mse - hcm_mse

    result = {
        "ar_mse": float(ar_mse),
        "hcm_mse": float(hcm_mse),
        "delta_mse": float(delta),
        "hcm_superior": bool(hcm_mse < ar_mse),
        "mse": float(mse)
    }

    print(json.dumps(result))


if __name__ == "__main__":
    run(sys.argv[1])
