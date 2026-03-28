import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

np.random.seed(42)

def generate_chaotic_series(n=1500):
    x = np.zeros(n)
    x[0] = 0.1

    for i in range(1, n):
        x[i] = 3.9 * x[i-1] * (1 - x[i-1]) + np.random.normal(0, 0.005)

    return x

series = generate_chaotic_series(1500)

# split
train = series[:1100]
test = series[1100:]

# build lag features
def build_features(data, lag=15):
    X, y = [], []
    for i in range(lag, len(data)):
        X.append(data[i-lag:i])
        y.append(data[i])
    return np.array(X), np.array(y)

X_train, y_train = build_features(train)
X_test, y_test = build_features(test)

# 🔥 nonlinear model (critical upgrade)
model = RandomForestRegressor(
    n_estimators=400,
    max_depth=12,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=1
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

df = pd.DataFrame({
    "y_true": y_test,
    "y_pred": y_pred
})

df.to_csv("data/predictions.csv", index=False)

print("High-quality nonlinear predictions generated.")
