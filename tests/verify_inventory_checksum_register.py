#!/usr/bin/env python3
"""Validate the six-file inventory checksum register from the artifacts/ directory."""
from pathlib import Path
import hashlib

root = Path("artifacts")
files = [
    root / "type1_governance_inventory" / "provenance.json",
    root / "type1_governance_inventory" / "reference_inventory.json",
    root / "type1_occurrence_ledger" / "occurrence_level_manual_ledger.json",
    root / "type1_occurrence_ledger" / "reconciliation.json",
    root / "type1_occurrence_ledger" / "main_occurrence_level_manual_ledger.json",
    root / "type1_occurrence_ledger" / "main_reconciliation.json",
]

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

missing = [str(path) for path in files if not path.is_file()]
if missing:
    raise SystemExit(f"BLOCKED: checksum input missing: {missing}")

expected = {path.relative_to(root).as_posix(): sha(path) for path in files}
checksum_file = root / "SHA256SUMS.txt"
lines = checksum_file.read_text(encoding="utf-8").splitlines()
if len(lines) != len(files):
    raise SystemExit(f"BLOCKED: expected {len(files)} physical checksum lines, found {len(lines)}")

actual = {}
for line in lines:
    parts = line.split("  ", 1)
    if len(parts) != 2 or len(parts[0]) != 64:
        raise SystemExit(f"BLOCKED: malformed checksum line: {line!r}")
    digest, relative_path = parts
    if relative_path in actual:
        raise SystemExit(f"BLOCKED: duplicate checksum path: {relative_path}")
    actual[relative_path] = digest

if actual != expected:
    raise SystemExit("BLOCKED: checksum register differs from actual artifact payload hashes")
print("INVENTORY_ARTIFACT_CHECKSUM_REGISTER_VERIFIED")
