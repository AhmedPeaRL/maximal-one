import numpy as np
import pandas as pd
from analysis.independent_validation import compare_methods

def generate_adversarial_signal(n=1000):
    # random walk + noise + fake structure
    x = np.cumsum(np.random.randn(n))
    noise = np.random.randn(n) * 0.5
    fake = np.sin(np.linspace(0, 20, n)) * 0.2
    return x + noise + fake

def run_test():
    real = pd.read_csv("real-data/sunspots_global.csv")
    col = "Sunspots" if "Sunspots" in real.columns else "value"

    print("=== REAL DATA ===")
    compare_methods(real[col].values)

    print("\n=== ADVERSARIAL DATA ===")
    adv = generate_adversarial_signal()
    
    try:
        if abs(a1 - a2) > 0.5:
            return "unstable/adversarial"
        else:
            return "valid structure"
            
        compare_methods(adv)
        print("⚠️ WARNING: adversarial passed (unexpected)")
    except SystemExit:
        print("✅ adversarial correctly rejected (robust)")

if __name__ == "__main__":
    run_test()
