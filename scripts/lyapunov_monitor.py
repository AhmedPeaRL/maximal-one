#!/usr/bin/env python3

import json
from pathlib import Path

STATE_FILE = Path("state/statistical-state.json")
LYAPUNOV_FILE = Path("state/lyapunov-history.json")


def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text())
    return default


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def main():
    state = load_json(STATE_FILE, None)
    if not state:
        print("NO_STATE")
        return

    variance = state.get("stddev", 0.0) ** 2

    history = load_json(LYAPUNOV_FILE, [])
    history.append(variance)

    save_json(LYAPUNOV_FILE, history)

    if len(history) < 5:
        print("LYAPUNOV=insufficient-data")
        return

    decreasing = all(history[i] >= history[i+1] for i in range(len(history)-1))

    if decreasing:
        print("LYAPUNOV=converging")
    else:
        print("LYAPUNOV=non-monotonic")


if __name__ == "__main__":
    main()
