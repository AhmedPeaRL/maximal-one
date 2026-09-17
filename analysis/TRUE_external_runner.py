from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

REPO = "https://github.com/AhmedPeaRL/maximal-one.git"
SEED = "42"

def run_checked(command, cwd=None):
    subprocess.run(
        command,
        cwd=cwd,
        check=True,
    )

def normalized_value(value):
    if isinstance(value, dict):
        return {
            key: normalized_value(value[key])
            for key in sorted(value)
            if key not in {
                "generated_at",
                "timestamp",
                "runtime",
                "environment",
            }
        }

    if isinstance(value, list):
        return [
            normalized_value(item)
            for item in value
        ]

    if isinstance(value, float):
        return round(value, 8)

    return value

def canonical_fingerprint(report):
    normalized = normalized_value(report)

    payload = json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return hashlib.sha256(
        payload
    ).hexdigest()

def load_json(path):
    with open(
        path,
        "r",
        encoding="utf-8",
    ) as handle:
        return json.load(handle)

def run_external():
    root = Path.cwd()

    local_report_path = (
        root
        /
        "artifacts"
        /
        "canonical_report.json"
    )

    if not local_report_path.exists():
        raise RuntimeError(
            "Local canonical report is missing"
        )

    local_report = load_json(
        local_report_path
    )

    local_fingerprint = canonical_fingerprint(
        local_report
    )

    tmp = Path(
        tempfile.mkdtemp(
            prefix="maximal_one_true_external_"
        )
    )

    try:
        repo_dir = tmp / "repo"
        env_dir = tmp / "venv"

        print(
            "Cloning repository into:",
            repo_dir,
        )

        run_checked(
            [
                "git",
                "clone",
                REPO,
                str(repo_dir),
            ]
        )

        target_sha = os.environ.get(
            "GITHUB_SHA"
        )

        if target_sha:
            print(
                "Checking out exact workflow commit:",
                target_sha,
            )

            run_checked(
                [
                    "git",
                    "fetch",
                    "origin",
                    target_sha,
                ],
                cwd=repo_dir,
            )

            run_checked(
                [
                    "git",
                    "checkout",
                    "--detach",
                    target_sha,
                ],
                cwd=repo_dir,
            )

        print(
            "Creating isolated Python environment..."
        )

        venv.create(
            str(env_dir),
            with_pip=True,
        )

        if os.name == "nt":
            external_python = (
                env_dir
                /
                "Scripts"
                /
                "python.exe"
            )
        else:
            external_python = (
                env_dir
                /
                "bin"
                /
                "python"
            )

        external_python = str(
            external_python
        )

        print(
            "Installing locked dependencies "
            "inside isolated environment..."
        )

        run_checked(
            [
                external_python,
                "-m",
                "pip",
                "install",
                "--no-cache-dir",
                "--requirement",
                "requirements-lock.txt",
            ],
            cwd=repo_dir,
        )

        print(
            "Running canonical pipeline "
            "inside isolated environment..."
        )

        run_checked(
            [
                external_python,
                "scripts/generate_report.py",
                "--seed",
                SEED,
                "--canonical",
            ],
            cwd=repo_dir,
        )

        external_report_path = (
            repo_dir
            /
            "artifacts"
            /
            "canonical_report.json"
        )

        if not external_report_path.exists():
            raise RuntimeError(
                "External canonical report was not generated"
            )

        external_report = load_json(
            external_report_path
        )

        external_fingerprint = (
            canonical_fingerprint(
                external_report
            )
        )

        structure_match = (
            isinstance(local_report, dict)
            and isinstance(external_report, dict)
            and set(local_report.keys())
            == set(external_report.keys())
        )

        fingerprint_match = (
            local_fingerprint
            ==
            external_fingerprint
        )

        result = {
            "independent_replay_verified": bool(
                fingerprint_match
                and structure_match
            ),
            "fingerprint_match": bool(
                fingerprint_match
            ),
            "structure_match": bool(
                structure_match
            ),
            "local_fingerprint": local_fingerprint,
            "external_fingerprint": external_fingerprint,
            "comparison_method": (
                "normalized_full_canonical_report"
            ),
            "normalization_precision": 8,
            "scientific_role": (
                "independent_clean_environment_reproducibility_gate"
            ),
            "verification_method": (
                "independent_clean_environment_rerun"
            ),
            "canonical_input_preparation": (
                "scripts/prepare_canonical_inputs.py"
            ),
            "status": (
                "verified"
                if (
                    fingerprint_match
                    and structure_match
                )
                else "failed"
            ),
        }

        output = (
            root
            /
            "artifacts"
            /
            "external_replay_verification.json"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            json.dumps(
                result,
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

        print(
            "LOCAL FINGERPRINT:",
            local_fingerprint,
        )

        print(
            "EXTERNAL FINGERPRINT:",
            external_fingerprint,
        )

        print(
            "STRUCTURE MATCH:",
            structure_match,
        )

        print(
            "FINGERPRINT MATCH:",
            fingerprint_match,
        )

        if not result[
            "independent_replay_verified"
        ]:
            raise RuntimeError(
                "TRUE external clean-environment "
                "reproduction failed"
            )

        print(
            "✅ TRUE EXTERNAL CLEAN-ENVIRONMENT "
            "REPRODUCTION VERIFIED"
        )

    finally:
        shutil.rmtree(
            tmp,
            ignore_errors=True,
        )

if __name__ == "__main__":
    run_external()
