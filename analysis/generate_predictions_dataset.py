import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

np.random.seed(42)

def generate_lorenz_like(n=1000):
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = 0.9 * x[i-1] + np.sin(x[i-1]) + np.random.normal(0, 0.1)
    return x

series = generate_lorenz_like(1200)

# split
train = series[:1000]
test = series[1000:]

# build lag features
def build_features(data, lag=5):
    X, y = [], []
    for i in range(lag, len(data)):
        X.append(data[i-lag:i])
        y.append(data[i])
    return np.array(X), np.array(y)

X_train, y_train = build_features(train)
X_test, y_test = build_features(test)

# train real model
model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

df = pd.DataFrame({
    "y_true": y_test,
    "y_pred": y_pred
})

df.to_csv("data/predictions.csv", index=False)

print("Real predictions generated.")
