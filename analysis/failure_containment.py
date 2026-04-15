import json
import os

SUMMARY_PATH = "artifacts/failure_summary.json"
OUTPUT = "artifacts/failure_verdict.json"


def main():
    if not os.path.exists(SUMMARY_PATH):
        verdict = {
            "status": "clean",
            "action": "continue"
        }
    else:
        with open(SUMMARY_PATH) as f:
            s = json.load(f)

        if s["critical"] > 0:
            verdict = {
                "status": "critical_failure",
                "action": "halt"
            }

        elif s["medium"] > 5:
            verdict = {
                "status": "degraded",
                "action": "continue_with_warning"
            }

        else:
            verdict = {
                "status": "stable",
                "action": "continue"
            }

    with open(OUTPUT, "w") as f:
        json.dump(verdict, f, indent=2)

    print("Containment Verdict:", verdict)


if __name__ == "__main__":
    main()
