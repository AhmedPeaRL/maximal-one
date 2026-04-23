import json
import sys

def check_self_reference():
    try:
        with open("artifacts/canonical_report.json") as f:
            report = json.load(f)
    except:
        print("❌ Missing report")
        sys.exit(1)

    if "_environment" not in report:
        print("❌ No external fingerprint → self-referential")
        sys.exit(1)

    if report.get("_sealed") != True:
        print("❌ Report not sealed → mutable truth")
        sys.exit(1)

    print("✅ Self-reference guarded")

if __name__ == "__main__":
    check_self_reference()
