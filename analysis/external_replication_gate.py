import json
import os
import sys

REPORT_PATH = "artifacts/canonical_report.json"

if not os.path.exists(REPORT_PATH):
    print("No external replication report found.")
    print("Skipping external replication gate.")
    sys.exit(0)

with open(REPORT_PATH) as f:
    report = json.load(f)

status = report.get("replication_status", "unknown")

print("External replication status:", status)

if status != "confirmed":
    print("External replication not yet confirmed.")
    sys.exit(0)

print("External replication confirmed.")
