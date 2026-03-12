import json
import os
import pandas as pd
from datetime import datetime

SCAN="artifacts/invariant_scan.json"
HISTORY="data/invariant_history.csv"

if not os.path.exists(SCAN):
    exit()

data=json.load(open(SCAN))

rows=[]
t=datetime.utcnow().isoformat()

for d in data:
    d["time"]=t
    rows.append(d)

df=pd.DataFrame(rows)

if os.path.exists(HISTORY):
    old=pd.read_csv(HISTORY)
    df=pd.concat([old,df])

df.to_csv(HISTORY,index=False)

print("history updated:",len(df))
