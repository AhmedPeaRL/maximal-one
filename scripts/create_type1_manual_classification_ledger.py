from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--inventory", required=True)
    p.add_argument("--expected-commit", required=True)
    p.add_argument("--output", default="artifacts/type1_manual_classification")
    a=p.parse_args()
    data=json.loads(Path(a.inventory).read_text(encoding="utf-8"))
    refs=[r for r in data.get("refs",[]) if r.get("commit_sha","").lower()==a.expected_commit.lower()]
    if data.get("audit")!="TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1" or len(refs)!=1:
        raise SystemExit("BLOCKED: inventory schema or exact commit identity mismatch.")
    ref=refs[0]
    rows=[]
    for entry in ref.get("entries",[]):
        path=entry["path"]
        prefix=hashlib.sha256(path.encode()).hexdigest()[:12]
        for index, match in enumerate(entry.get("matches",[]),1):
            line=match["line"]
            rows.append({
                "occurrence_id":f"{ref.get('ref_requested')}/{prefix}/{line}/{index}",
                "repository_ref":ref.get("ref_requested"),
                "commit_sha":ref["commit_sha"],
                "path":path,
                "line":line,
                "exact_matched_text":match.get("text",""),
                "automated_inventory_classification":match.get("classification","UNKNOWN"),
                "manual_classification":"UNKNOWN",
                "historical_diagnostic_proposed_governance_status":"UNDETERMINED",
                "can_influence_execution":"UNKNOWN",
                "direct_caller_or_workflow_step":"OPEN",
                "indirect_call_path":"OPEN",
                "runner_entry_point_or_command":"OPEN",
                "trigger_conditions_and_branch_restrictions":"OPEN",
                "matrix_and_protocol_consumed":"OPEN",
                "authorization_guard_and_execution_order":"OPEN",
                "guard_fails_closed":"UNKNOWN",
                "negative_test":"NOT_YET_IDENTIFIED",
                "test_run_job_artifact_commit":"OPEN",
                "reviewer_disposition":"PENDING",
                "status":"OPEN",
                "closure_evidence":None,
                "unresolved_reason":"Manual inspection required; automated classification is not final."
            })
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    target=out/"occurrence_level_manual_ledger.json"
    target.write_text(json.dumps({
        "schema":"HCM_TYPE1_OCCURRENCE_MANUAL_LEDGER_V1",
        "inventory_commit":ref["commit_sha"],
        "inventory_ref":ref.get("ref_requested"),
        "occurrence_count":len(rows),
        "authority":"DISCOVERY_TEMPLATE_ONLY_NOT_APPROVAL",
        "records":rows
    },indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(f"Wrote {target} with {len(rows)} OPEN occurrence records.")
    print("No occurrence was manually classified or closed.")
if __name__=="__main__":
    main()
