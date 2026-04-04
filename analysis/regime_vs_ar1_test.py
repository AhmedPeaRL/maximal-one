import numpy as np
from statsmodels.tsa.ar_model import AutoReg
from regime_shift_advanced import detect_regime_shift_advanced

def generate_regime_data(n=500):
    x = []

    for i in range(n):
        if i < n//2:
            x.append(np.sin(i/10) + np.random.normal(0, 0.2))
        else:
            x.append(2*np.sin(i/5) + np.random.normal(0, 0.5))

    return np.array(x)


def test_regime_detection():
    data = generate_regime_data()

    # AR(1)
    model = AutoReg(data, lags=1).fit()
    preds = model.predict(start=1, end=len(data)-1)

    ar1_error = np.mean((data[1:] - preds)**2)

    # HCM regime detection
    shifts = detect_regime_shift_advanced(data)

    return {
        "ar1_mse": float(ar1_error),
        "num_detected_shifts": len(shifts),
        "shift_positions": shifts[:5]
    }


if __name__ == "__main__":
    result = test_regime_detection()
    print(result)
