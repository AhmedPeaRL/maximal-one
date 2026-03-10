import hashlib
import json
import pathlib

DATA_DIR = pathlib.Path("real-data")
MANIFEST = pathlib.Path("artifacts/dataset_manifest.json")

def file_hash(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

manifest = {}

if DATA_DIR.exists():
    for f in DATA_DIR.glob("*.csv"):
        manifest[f.name] = file_hash(f)

MANIFEST.parent.mkdir(exist_ok=True)

with open(MANIFEST,"w") as out:
    json.dump(manifest,out,sort_keys=True,indent=2)

print("Dataset manifest generated.")
