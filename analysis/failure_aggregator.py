import json
import os

FAILURE_LOG = "artifacts/failure_log.json"
OUTPUT = "artifacts/failure_summary.json"


def main():
    if not os.path.exists(FAILURE_LOG):
        summary = {
            "total": 0,
            "critical": 0,
            "medium": 0,
            "low": 0
        }
    else:
        with open(FAILURE_LOG) as f:
            data = json.load(f)

        summary = {
            "total": len(data),
            "critical": sum(1 for x in data if x["severity"] == "critical"),
            "medium": sum(1 for x in data if x["severity"] == "medium"),
            "low": sum(1 for x in data if x["severity"] == "low")
        }

    with open(OUTPUT, "w") as f:
        json.dump(summary, f, indent=2)

    print("Failure Summary:", summary)


if __name__ == "__main__":
    main()
