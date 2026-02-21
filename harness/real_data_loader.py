#!/usr/bin/env python3
import pandas as pd
import sys

def load(path):
    df = pd.read_csv(path)
    if df.shape[1] == 1:
        return df.iloc[:,0].values
    return df.select_dtypes(include="number").mean(axis=1).values

if __name__ == "__main__":
    data = load(sys.argv[1])
    for x in data:
        print(float(x))
