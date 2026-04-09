import json, os

def check():
    if not os.path.exists("data/decision_lineage.json"):
        return

    with open("data/decision_lineage.json") as f:
        data = json.load(f)

    if len(data) < 2:
        return

    last = data[-1]
    prev = data[-2]

    if last["decision"] == prev["decision"]:
        print("Continuity stable.")
    else:
        print("Continuity shift detected.")

if __name__ == "__main__":
    check()
