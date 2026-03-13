import json
import os
import datetime

SRC="artifacts/hypotheses.json"
DST="data/hypothesis_history.json"

if os.path.exists(SRC):
    h=json.load(open(SRC))

    entry={
        "timestamp":datetime.datetime.utcnow().isoformat(),
        "count":len(h),
        "hypotheses":h
    }

    hist=[]
    if os.path.exists(DST):
        hist=json.load(open(DST))

    hist.append(entry)

    with open(DST,"w") as f:
        json.dump(hist,f,indent=2)

    print("History updated.")
else:
    print("No hypotheses found.")
