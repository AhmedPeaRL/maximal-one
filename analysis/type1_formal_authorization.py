from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


AUTHORIZED_REF = "refs/heads/review/type1-v4-remediation"

MATRIX_PATH = Path(
    "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json"
)
FREEZE_PATH = Path(
    "protocol/TYPE1_CALIBRATION_FREEZE_DECISION.json"
)
AUTH_PATH = Path(
    "protocol/TYPE1_CALIBRATION_EXECUTION_AUTHORIZATION.json"
)

REQUIRED_SOURCE_PATHS = [
    "analysis/calibrate_null_type1.py",
    "analysis/calibrate_null_type1_scenario.py",
    "analysis/appropriate_stochastic_null.py",
    "analysis/numerical_spectral_verification.py",
    "analysis/type1_formal_authorization.py",
    "requirements-lock.txt",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(root: Path, relative_path: Path) -> dict:
    path = root / relative_path
    if not path.is_file():
        raise SystemExit(f"BLOCKED: missing authorization file: {relative_path}")

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(
            f"BLOCKED: invalid JSON in {relative_path}: {exc}"
        ) from exc

    if not isinstance(value, dict):
        raise SystemExit(f"BLOCKED: expected JSON object: {relative_path}")

    return value


def git_head(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception as exc:
        raise SystemExit(
            "BLOCKED: cannot establish exact Git checkout identity."
        ) from exc


def require_formal_authorization(root: Path | None = None) -> dict:
    root = (root or Path(__file__).resolve().parents[1]).resolve()

    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise SystemExit(
            "BLOCKED: formal calibration requires GitHub Actions context."
        )

    if os.environ.get("GITHUB_REF") != AUTHORIZED_REF:
        raise SystemExit(
            "BLOCKED: formal calibration is restricted to "
            f"{AUTHORIZED_REF}."
        )

    expected_sha = os.environ.get("GITHUB_SHA", "").strip()
    actual_sha = git_head(root)

    if not expected_sha or actual_sha != expected_sha:
        raise SystemExit(
            "BLOCKED: GITHUB_SHA does not match the checked-out HEAD."
        )

    matrix = load_json(root, MATRIX_PATH)
    freeze = load_json(root, FREEZE_PATH)
    authorization = load_json(root, AUTH_PATH)

    matrix_path = root / MATRIX_PATH
    freeze_path = root / FREEZE_PATH

    matrix_sha = sha256_file(matrix_path)
    freeze_sha = sha256_file(freeze_path)

    # The existing candidate schema is deliberately not approvable.
    design = matrix.get("approved_design")
    if not isinstance(design, dict):
        raise SystemExit(
            "BLOCKED: matrix has no independently approved_design. "
            "Candidate dimensions cannot authorize execution."
        )

    if matrix.get("status") != "APPROVED_FROZEN":
        raise SystemExit("BLOCKED: matrix is not APPROVED_FROZEN.")

    if matrix.get("freeze_state") != "FROZEN":
        raise SystemExit("BLOCKED: matrix freeze_state is not FROZEN.")

    if matrix.get("confirmatory_execution_authorized") is not True:
        raise SystemExit(
            "BLOCKED: matrix does not explicitly authorize confirmatory execution."
        )

    if freeze.get("decision_status") != "APPROVED":
        raise SystemExit("BLOCKED: freeze decision is not APPROVED.")

    if freeze.get("freeze_state") != "FROZEN":
        raise SystemExit("BLOCKED: freeze decision is not FROZEN.")

    if freeze.get("reviewed_commit_sha") != actual_sha:
        raise SystemExit("BLOCKED: freeze decision targets another commit.")

    if not freeze.get("reviewer_identity"):
        raise SystemExit("BLOCKED: reviewer identity is missing.")

    if freeze.get("reviewer_independence_verified") is not True:
        raise SystemExit(
            "BLOCKED: independent reviewer status is not verified."
        )

    if freeze.get("reviewed_file_sha256") != matrix_sha:
        raise SystemExit(
            "BLOCKED: freeze decision does not bind the exact matrix hash."
        )

    dispositions = freeze.get("parameter_dispositions")
    if not isinstance(dispositions, dict) or not dispositions:
        raise SystemExit("BLOCKED: parameter dispositions are missing.")

    if any(
        value in (None, "", "UNRESOLVED", "PENDING")
        for value in dispositions.values()
    ):
        raise SystemExit("BLOCKED: one or more parameters remain unresolved.")

    required_tests = freeze.get("required_tests")
    if not isinstance(required_tests, dict) or not required_tests:
        raise SystemExit("BLOCKED: required test evidence is missing.")

    if any(value != "PASSED" for value in required_tests.values()):
        raise SystemExit("BLOCKED: not all required engineering tests passed.")

    if authorization.get("authorization_status") != "AUTHORIZED":
        raise SystemExit("BLOCKED: execution authorization is not AUTHORIZED.")

    if authorization.get("frozen_commit_sha") != actual_sha:
        raise SystemExit("BLOCKED: authorization targets another commit.")

    if authorization.get("freeze_decision_file_sha256") != freeze_sha:
        raise SystemExit(
            "BLOCKED: authorization does not bind the exact freeze decision."
        )

    if authorization.get("authorized_matrix_sha256") != matrix_sha:
        raise SystemExit(
            "BLOCKED: authorization does not bind the exact matrix."
        )

    if not authorization.get("authorized_decision_maker"):
        raise SystemExit("BLOCKED: authorized decision maker is missing.")

    if not authorization.get("authorized_entrypoint"):
        raise SystemExit("BLOCKED: authorized entry point is missing.")

    if not authorization.get("authorized_scenarios"):
        raise SystemExit("BLOCKED: authorized scenario list is empty.")

    matrix_scenarios = [
        row.get("scenario_id")
        for row in matrix.get("scenarios", [])
    ]

    if authorization["authorized_scenarios"] != matrix_scenarios:
        raise SystemExit(
            "BLOCKED: authorized scenarios do not exactly match the matrix."
        )

    if design.get("acceptance_rule") in (None, {}, ""):
        raise SystemExit("BLOCKED: acceptance rule is unresolved.")

    if not isinstance(design.get("invalid_attempt_policy"), dict):
        raise SystemExit("BLOCKED: invalid-attempt policy is missing.")

    source_hashes = authorization.get("authorized_source_hashes")
    if not isinstance(source_hashes, dict):
        raise SystemExit("BLOCKED: authorized source hash map is missing.")

    for relative in REQUIRED_SOURCE_PATHS:
        expected_hash = source_hashes.get(relative)
        path = root / relative

        if not expected_hash or not path.is_file():
            raise SystemExit(
                f"BLOCKED: missing authorized source hash or file: {relative}"
            )

        if sha256_file(path) != expected_hash:
            raise SystemExit(
                f"BLOCKED: source hash mismatch: {relative}"
            )

    return {
        "status": "AUTHORIZED_PREFLIGHT_PASSED",
        "commit_sha": actual_sha,
        "matrix_sha256": matrix_sha,
        "freeze_sha256": freeze_sha,
        "formal_calibration_started": False,
        "claim_support": False,
        "promotion_authority": False,
    }
