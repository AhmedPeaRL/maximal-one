import numpy as np
from statsmodels.tsa.ar_model import AutoReg
from scipy.stats import ttest_rel
import sys
import json

np.random.seed(42)

def generate_hcm_series(n=2000):
    x = np.zeros(n)
    for i in range(1,n):
        x[i] = 0.85*x[i-1] + 0.1*np.sin(x[i-1]) + np.random.normal(0,0.05)
    return x

def random_walk(n=2000):
    return np.cumsum(np.random.normal(0,1,n))

def fbm_like(n=2000, hurst=0.75):
    noise = np.random.normal(0,1,n)
    return np.cumsum(noise * (np.arange(n)+1)**(hurst-0.5))

def mse(a,b):
    return np.mean((a-b)**2)

def evaluate(series):
    train = series[:1500]
    test = series[1500:]
    
    ar = AutoReg(train,lags=1,old_names=False).fit()
    ar_pred = ar.predict(start=1500,end=len(series)-1)
    
    hcm_pred = train[-1]
    preds=[]
    for i in range(len(test)):
        hcm_pred = 0.85*hcm_pred + 0.1*np.sin(hcm_pred)
        preds.append(hcm_pred)
    
    return mse(test,ar_pred), mse(test,np.array(preds))

series = generate_hcm_series()
ar_mse, hcm_mse = evaluate(series)

delta = ar_mse - hcm_mse

result = {
    "ar_mse": ar_mse,
    "hcm_mse": hcm_mse,
    "delta_mse": delta,
    "passed": delta > 0
}

print(json.dumps(result))

if delta <= 0:
    print("Predictive superiority failed.")
    sys.exit(1)
