import time
import os
import json

START_TIME = time.time()

# ⛔ MAX RUNTIME (in seconds)
MAX_RUNTIME = 1200  # 20 minutes hard cap

# ⛔ MAX DATA SIZE (MB)
MAX_DATA_SIZE_MB = 500

def get_dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total / (1024 * 1024)

def enforce_runtime():
    elapsed = time.time() - START_TIME
    if elapsed > MAX_RUNTIME:
        print("⛔ Runtime limit exceeded")
        exit(1)

def enforce_data_limit():
    if os.path.exists("real-data"):
        size = get_dir_size("real-data")
        print(f"Dataset size: {size:.2f} MB")
        if size > MAX_DATA_SIZE_MB:
            print("⛔ Dataset size exceeded limit")
            exit(1)

def checkpoint():
    enforce_runtime()
    enforce_data_limit()

def final_report():
    report = {
        "runtime_sec": time.time() - START_TIME,
        "status": "bounded"
    }
    with open("artifacts/runtime_guard.json", "w") as f:
        json.dump(report, f)
