#!/usr/bin/env python3
"""Convert a filled V2 adjudication CSV into a commit-bound V2 JSON overlay."""
import argparse, csv, json, sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--csv",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    with open(a.csv,encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    if not rows: raise SystemExit("No CSV rows found")
    first=rows[0]
    required_meta=("inventory_commit","inventory_ref","inventory_sha256")
    if any(not first.get(k) for k in required_meta): raise SystemExit("Missing inventory binding")
    for row in rows:
        for k in required_meta:
            if row.get(k)!=first[k]: raise SystemExit(f"Mixed inventory identity in CSV: {k}")
    records=[]
    fields=("occurrence_id","manual_classification","can_influence_execution","direct_caller_or_workflow_step",
            "indirect_call_path","runner_entry_point_or_command","trigger_conditions_and_branch_restrictions",
            "matrix_and_protocol_consumed","authorization_guard_and_execution_order","guard_fails_closed",
            "negative_test","test_run_job_artifact_commit","historical_diagnostic_proposed_governance_status",
            "reviewer","reviewer_role","conflict_statement","reviewed_at_utc","rationale","status","reviewer_disposition")
    for i,row in enumerate(rows,2):
        disp=(row.get("reviewer_disposition") or "PENDING").strip()
        if disp!="ADJUDICATED": continue
        record={k:(row.get(k) or "").strip() for k in fields}
        raw=(row.get("closure_evidence") or "").strip()
        if raw:
            try: record["closure_evidence"]=json.loads(raw)
            except Exception as e: raise SystemExit(f"CSV row {i}: closure_evidence must be JSON: {e}")
        else: record["closure_evidence"]=None
        records.append(record)
    out={"schema":"HCM_TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V2",
         "review_commit_sha":first["inventory_commit"],"inventory_ref":first["inventory_ref"],
         "inventory_sha256":first["inventory_sha256"],"records":records}
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"OVERLAY_WRITTEN records={len(records)} total_csv_rows={len(rows)}")
    print("Unadjudicated rows are omitted from the overlay and remain OPEN/UNKNOWN in the source ledger.")
if __name__=="__main__": main()
