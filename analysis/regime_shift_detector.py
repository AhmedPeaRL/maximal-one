import numpy as np

def detect_regime_shift(signal, window=10, threshold=2.0):
    signal = np.array(signal)
    
    shifts = []
    
    for i in range(window, len(signal) - window):
        past = signal[i-window:i]
        future = signal[i:i+window]
        
        past_mean = np.mean(past)
        future_mean = np.mean(future)
        
        diff = abs(future_mean - past_mean)
        std = np.std(signal)
        
        if std == 0:
            continue
        
        score = diff / std
        
        if score > threshold:
            shifts.append({
                "index": i,
                "score": float(score),
                "past_mean": float(past_mean),
                "future_mean": float(future_mean)
            })
    
    return shifts
