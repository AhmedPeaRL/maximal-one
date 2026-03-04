import numpy as np
from sklearn.linear_model import Ridge

def delay_embedding(x, dim=3, tau=1):
    N = len(x) - (dim - 1) * tau
    return np.array([x[i:i+dim*tau:tau] for i in range(N)])

def ridge_predict(x, horizon=1):
    emb = delay_embedding(x)
    y = x[(len(x)-len(emb)) + horizon:]
    X = emb[:-horizon]
    y = y[:len(X)]

    model = Ridge(alpha=1.0)
    model.fit(X, y)
    pred = model.predict(X)

    mse = np.mean((pred - y)**2)
    return mse
