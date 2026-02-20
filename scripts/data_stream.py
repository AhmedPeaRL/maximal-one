#!/usr/bin/env python3

import json
import csv
import sys
from pathlib import Path

def extract_scores(path):
    path = Path(path)

    if path.suffix == ".json":
        data = json.loads(path.read_text())
        return [float(x) for x in data]

    if path.suffix == ".csv":
        scores = []
        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:
                scores.append(float(row[0]))
        return scores

    raise ValueError("Unsupported file format")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: data_stream.py <file>")
        sys.exit(1)

    scores = extract_scores(sys.argv[1])

    for s in scores:
        print(s)
