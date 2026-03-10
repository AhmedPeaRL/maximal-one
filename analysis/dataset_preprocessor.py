import pandas as pd
import numpy as np
import sys
from pathlib import Path

def prepare_dataset(path):
    df = pd.read_csv(path)
    
    for col in df.columns:
       df[col] = pd.to_numeric(df[col], errors="coerce")
    
    df = df.dropna()

    # keep numeric columns only
    df = df.select_dtypes(include=[np.number])

    if df.shape[1] == 0:
        raise ValueError("No numeric columns found")

    # take first numeric column
    series = df.iloc[:,0].dropna()

    # normalize
    series = (series - series.mean()) / series.std()

    out = Path(path).with_name(Path(path).stem + "_prepared.csv")

    series.to_csv(out, index=False)

    print("prepared dataset:", out)

if __name__ == "__main__":
    prepare_dataset(sys.argv[1])
