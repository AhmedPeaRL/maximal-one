from __future__ import annotations

import hashlib
import json
from pathlib import Path

from analysis.canonical_json import canonicalize

ARTIFACTS = Path("artifacts")

REQUIRED = [
    "canonical_report.json",
    "report.hash",
    "report_hash_manifest.json",
    "external_replay_verification.json",
    "adversarial_control.json",
    "artifact_closure.json",
    "witness_lock.json",
    "release_manifest.json",
    "reproducibility_manifest.json",
    "reproducibility_stamp.json",
    "temporal_sovereignty.json",
    "final_state_lock.json",
]

def fail(message: str) -> None:
    raise SystemExit(
        "FINAL PROVENANCE CLOSURE FAILURE: "
        + message
    )

def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()

def load_json(name: str) -> dict:
    path = ARTIFACTS / name

    require(
        path.exists(),
        f"missing {name}",
    )

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        fail(
            f"invalid JSON in {name}: {exc}"
        )

def verify_required_files() -> None:
    for name in REQUIRED:
        require(
            (ARTIFACTS / name).exists(),
            f"missing required artifact: {name}",
        )

def verify_report_hash() -> None:
    actual = sha256_file(
        ARTIFACTS / "canonical_report.json"
    )

    declared = (
        ARTIFACTS
        / "report.hash"
    ).read_text(
        encoding="utf-8"
    ).strip()

    require(
        declared == actual,
        "report.hash does not match canonical_report.json",
    )

    stamp = load_json(
        "reproducibility_stamp.json"
    )

    require(
        stamp.get("artifact")
        == "canonical_report.json",
        "reproducibility stamp points to wrong artifact",
    )

    require(
        stamp.get("sealed") is True,
        "reproducibility stamp is not sealed",
    )

    require(
        stamp.get("sha256") == actual,
        "reproducibility stamp does not match canonical report",
    )

def verify_report_hash_manifest() -> None:
    report = load_json(
        "canonical_report.json"
    )

    manifest = load_json(
        "report_hash_manifest.json"
    )

    expected = hashlib.sha256(
        canonicalize(report).encode("utf-8")
    ).hexdigest()

    require(
        manifest.get("canonical_sha256")
        == expected,
        "report_hash_manifest does not match canonical report",
    )

def verify_external_replay() -> None:
    replay = load_json(
        "external_replay_verification.json"
    )

    require(
        replay.get("independent_replay_verified")
        is True,
        "independent replay is not verified",
    )

    require(
        replay.get("fingerprint_match")
        is True,
        "independent fingerprint does not match",
    )

    require(
        replay.get("structure_match")
        is True,
        "independent structure does not match",
    )

    require(
        replay.get("status")
        == "verified",
        "external replay status is not verified",
    )

    require(
        replay.get("scientific_role")
        == "independent_reproducibility_gate",
        "external replay role is invalid",
    )

def verify_adversarial_control() -> None:
    adversarial = load_json(
        "adversarial_control.json"
    )

    require(
        adversarial.get("passed")
        is True,
        "adversarial control did not pass",
    )

    require(
        adversarial.get("scientific_claim_authority")
        is False,
        "adversarial control incorrectly claims scientific authority",
    )

def verify_artifact_closure() -> None:
    closure = load_json(
        "artifact_closure.json"
    )

    hashes = closure.get(
        "hashes"
    )

    require(
        isinstance(hashes, dict),
        "artifact_closure.hashes is invalid",
    )

    require(
        closure.get("frozen") is True,
        "artifact closure is not frozen",
    )

    for name, expected in hashes.items():
        path = ARTIFACTS / name

        require(
            path.exists(),
            f"artifact_closure references missing artifact: {name}",
        )

        actual = sha256_file(path)

        require(
            actual == expected,
            f"artifact_closure hash mismatch: {name}",
        )

    require(
        closure.get("artifact_count")
        == len(hashes),
        "artifact_closure artifact_count mismatch",
    )

def verify_release_manifest() -> None:
    manifest = load_json(
        "release_manifest.json"
    )

    entries = manifest.get(
        "manifest"
    )

    require(
        isinstance(entries, dict),
        "release manifest is invalid",
    )

    for name, metadata in entries.items():
        path = ARTIFACTS / name

        require(
            path.exists(),
            f"release manifest references missing artifact: {name}",
        )

        actual_sha = sha256_file(path)

        require(
            actual_sha
            == metadata.get("sha256"),
            f"release manifest hash mismatch: {name}",
        )

        require(
            path.stat().st_size
            == metadata.get("size"),
            f"release manifest size mismatch: {name}",
        )

    require(
        manifest.get("artifact_count")
        == len(entries),
        "release manifest artifact_count mismatch",
    )

def verify_reproducibility_manifest() -> None:
    manifest = load_json(
        "reproducibility_manifest.json"
    )

    require(
        manifest.get("reproducibility_status")
        == "verified",
        "reproducibility manifest is not verified",
    )

    replay = load_json(
        "external_replay_verification.json"
    )

    require(
        manifest.get("independent_rerun_verified")
        is True,
        "reproducibility manifest says independent rerun failed",
    )

    require(
        manifest.get("fingerprint_match")
        is True,
        "reproducibility manifest says fingerprint mismatch",
    )

    require(
        manifest.get("structure_match")
        is True,
        "reproducibility manifest says structure mismatch",
    )

    require(
        manifest.get("local_fingerprint")
        == replay.get("local_fingerprint"),
        "local fingerprint differs from reproducibility manifest",
    )

    require(
        manifest.get("external_fingerprint")
        == replay.get("external_fingerprint"),
        "external fingerprint differs from reproducibility manifest",
    )

    require(
        manifest.get("canonical_report_sha256")
        == sha256_file(
            ARTIFACTS / "canonical_report.json"
        ),
        "reproducibility manifest canonical report hash mismatch",
    )

def verify_witness_lock() -> None:
    witness = load_json(
        "witness_lock.json"
    )

    declared_lock = witness.get(
        "witness_lock"
    )

    require(
        isinstance(declared_lock, str)
        and len(declared_lock) == 64,
        "witness_lock hash is invalid",
    )

    payload = dict(witness)
    payload.pop(
        "witness_lock",
        None
    )

    recomputed = hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True
        ).encode("utf-8")
    ).hexdigest()

    require(
        recomputed == declared_lock,
        "witness_lock self-hash mismatch",
    )

    for path_name, expected in payload.items():
        if not path_name.startswith(
            "artifacts/"
        ):
            continue

        path = Path(path_name)

        require(
            path.exists(),
            f"witness lock references missing artifact: {path_name}",
        )

        actual = sha256_file(path)

        require(
            actual == expected,
            f"witness lock hash mismatch: {path_name}",
        )

    strict_claim = Path(
        "core-scientific/strict_claim.json"
    )

    require(
        strict_claim.exists(),
        "strict_claim.json is missing",
    )

    strict_claim_hash = sha256_file(
        strict_claim
    )

    declared_contract_hash = witness.get(
        "core-scientific/strict_claim.json"
    )

    require(
        declared_contract_hash
        == strict_claim_hash,
        "witness lock is not bound to the authoritative strict claim",
    )

def verify_temporal_sovereignty() -> None:
    temporal = load_json(
        "temporal_sovereignty.json"
    )

    hashes = temporal.get(
        "hashes"
    )

    require(
        isinstance(hashes, dict),
        "temporal sovereignty hashes are invalid",
    )

    require(
        temporal.get("status")
        == "TEMPORAL_SOVEREIGNTY_HOLDS",
        "temporal sovereignty status is invalid",
    )

    for name, expected in hashes.items():
        path = ARTIFACTS / name

        require(
            path.exists(),
            f"temporal sovereignty references missing artifact: {name}",
        )

        require(
            sha256_file(path)
            == expected,
            f"temporal sovereignty hash mismatch: {name}",
        )

    require(
        temporal.get("artifact_count")
        == len(hashes),
        "temporal sovereignty artifact_count mismatch",
    )

def verify_final_state_lock() -> None:
    lock = load_json(
        "final_state_lock.json"
    )

    names = lock.get(
        "artifacts"
    )

    require(
        isinstance(names, list),
        "final_state_lock artifacts list is invalid",
    )

    require(
        lock.get("sealed") is True,
        "final state lock is not sealed",
    )

    combined = hashlib.sha256()

    for name in sorted(names):
        path = ARTIFACTS / name

        require(
            path.exists(),
            f"final state lock references missing artifact: {name}",
        )

        combined.update(
            path.read_bytes()
        )

    expected = combined.hexdigest()

    require(
        lock.get("final_state_hash")
        == expected,
        "final state lock hash mismatch",
    )

    require(
        lock.get("artifact_count")
        == len(names),
        "final state lock artifact_count mismatch",
    )

def main() -> None:
    verify_required_files()
    verify_report_hash()
    verify_report_hash_manifest()
    verify_external_replay()
    verify_adversarial_control()
    verify_artifact_closure()
    verify_release_manifest()
    verify_reproducibility_manifest()
    verify_witness_lock()
    verify_temporal_sovereignty()
    verify_final_state_lock()

    print(
        "=============================================="
    )
    print(
        "FINAL PROVENANCE CLOSURE VERIFIED"
    )
    print(
        "=============================================="
    )
    print(
        "Canonical report integrity: VERIFIED"
    )
    print(
        "Independent replay: VERIFIED"
    )
    print(
        "Fingerprint equality: VERIFIED"
    )
    print(
        "Adversarial control: VERIFIED"
    )
    print(
        "Artifact closure: VERIFIED"
    )
    print(
        "Release manifest: VERIFIED"
    )
    print(
        "Witness lock: VERIFIED"
    )
    print(
        "Temporal sovereignty: VERIFIED"
    )
    print(
        "Final state lock: VERIFIED"
    )
    print(
        "Authoritative strict claim binding: VERIFIED"
    )
    print(
        "=============================================="
    )

if __name__ == "__main__":
    main()
