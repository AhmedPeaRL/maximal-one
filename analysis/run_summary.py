import json
import os
import datetime
from pathlib import Path

artifacts = Path("artifacts")
artifacts.mkdir(exist_ok=True)

summary = {
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    "status": "run_completed",
    "files_present": [],
}

for f in artifacts.glob("*"):
    summary["files_present"].append(f.name)

with open(artifacts / "run_summary.json","w") as f:
    json.dump(summary,f,indent=2)

print("Run summary generated.")
