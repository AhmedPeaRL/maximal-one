import json
import os
from datetime import datetime

HISTORY="data/invariant_history.json"

def load():

    if os.path.exists(HISTORY):
        return json.load(open(HISTORY))

    return []

def main():

    hist=load()

    new=json.load(open("artifacts/invariants.json"))

    entry={
        "time":datetime.utcnow().isoformat(),
        "results":new
    }

    hist.append(entry)

    os.makedirs("data",exist_ok=True)

    json.dump(hist,open(HISTORY,"w"),indent=2)

if __name__=="__main__":
    main()
