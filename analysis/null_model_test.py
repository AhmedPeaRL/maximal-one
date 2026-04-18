import numpy as np
import json

def generate_null(series):
  return np.random.permutation(series)

def compare_alpha(real_alpha, null_alpha):
  return abs(real_alpha - null_alpha)

def main():
  
  with open("artifacts/windowed_spectral.json") as f:
    data = json.load(f)
    
    results = {}

    for name, windows in data.items():
      
      diffs = []
      
      for w in windows:
        real_alpha = w["alpha"]

        null_series = np.random.normal(0,1,512)
        null_alpha = np.mean(null_series)

        diffs.append(compare_alpha(real_alpha, null_alpha))
        
      results[name] = {
        "mean_separation": float(np.mean(diffs))
      }

    with open("artifacts/null_comparison.json","w") as f:
      json.dump(results,f,indent=2)

if name == "main":
  main()
