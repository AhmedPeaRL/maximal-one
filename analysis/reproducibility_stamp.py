import hashlib
import json
import numpy as np

def generate_stamp(report_path):
    with open(report_path, "rb") as f:
        content = f.read()

    return hashlib.sha256(content).hexdigest()


def attach_stamp(report_path):
    with open(report_path) as f:
        data = json.load(f)

    stamp = generate_stamp(report_path)
    data["reproducibility_stamp"] = stamp

    with open(report_path, "w") as f:
        json.dump(data, f, indent=2)

    return stamp


def simple_forecast(series, steps=10):
    series = np.asarray(series)

    coef = np.polyfit(np.arange(len(series)), series, 1)

    future = []
    for i in range(steps):
        x = len(series) + i
        future.append(coef[0]*x + coef[1])

    return np.array(future)


def evaluate_prediction(series):
    split = int(len(series) * 0.8)

    train = series[:split]
    test = series[split:]

    pred = simple_forecast(train, len(test))

    mse = np.mean((pred - test) ** 2)

    return float(mse)
