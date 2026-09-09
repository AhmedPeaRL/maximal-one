import subprocess
import tempfile
import os
import hashlib
import json
import shutil

REPO_URL = "https://github.com/ahmedpearl/maximal-one.git"

VOLATILE_KEYS = {
    "timestamp",
    "_environment",
    "_sealed",
    "generated_at",
    "runtime",
    "execution_time",
    "host",
}

def sha256_text(data):
    return hashlib.sha256(
        data.encode("utf-8")
    ).hexdigest()

def run_fresh_clone():
    tmp = tempfile.mkdtemp(
        prefix="maximal_one_reproduction_"
    )

    print("Cloning fresh repository...")

    subprocess.run(
        [
            "git",
            "clone",
            "--filter=blob:none",
            REPO_URL,
            tmp,
        ],
        check=True,
    )

    return tmp

def normalize_object(obj):
    if isinstance(obj, dict):
        return {
            key: normalize_object(value)
            for key, value in sorted(obj.items())
            if key not in VOLATILE_KEYS
        }

    if isinstance(obj, list):
        return [
            normalize_object(value)
            for value in obj
        ]

    if isinstance(obj, float):
        return float(
            format(obj, ".8f")
        )

    return obj

def normalize_report(raw):
    data = json.loads(raw)

    cleaned = normalize_object(data)

    return json.dumps(
        cleaned,
        sort_keys=True,
        separators=(",", ":"),
    )

def load_report(path):
    with open(
        path,
        "r",
        encoding="utf-8",
    ) as f:
        return f.read()

def run_pipeline(path):
    print(
        "Running independent canonical pipeline..."
    )

    env = os.environ.copy()

    env.update({
        "PYTHONHASHSEED": "42",
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
    })

    subprocess.run(
        [
            "python",
            "scripts/generate_report.py",
            "--seed",
            "42",
            "--canonical",
        ],
        cwd=path,
        check=True,
        env=env,
    )

    report_path = os.path.join(
        path,
        "artifacts",
        "canonical_report.json",
    )

    if not os.path.exists(report_path):
        raise RuntimeError(
            "Independent pipeline did not produce canonical_report.json"
        )

    return load_report(
        report_path
    )

def extract_required_structure(data):
    return {
        "spectral_profile": {
            "estimated_alpha":
                data["spectral_profile"]["estimated_alpha"],
            "bootstrap_mean":
                data["spectral_profile"]["bootstrap_mean"],
            "bootstrap_std":
                data["spectral_profile"]["bootstrap_std"],
        },
        "statistical_test": {
            "p_value":
                data["statistical_test"]["p_value"],
            "valid":
                data["statistical_test"]["valid"],
        },
        "cross_method_validation": {
            "primary_method":
                data["cross_method_validation"]["primary_method"],
            "validation_method":
                data["cross_method_validation"]["validation_method"],
            "agreement_delta":
                data["cross_method_validation"]["agreement_delta"],
        },
        "dataset_audit": {
            "analysis_length":
                data["dataset_audit"]["analysis_length"],
            "analysis_sha256":
                data["dataset_audit"]["analysis_sha256"],
        },
    }

def compare():
    local_report_path = os.path.join(
        "artifacts",
        "canonical_report.json",
    )

    if not os.path.exists(
        local_report_path
    ):
        raise RuntimeError(
            "Local canonical report is missing"
        )

    local_raw = load_report(
        local_report_path
    )

    local_norm = normalize_report(
        local_raw
    )

    local_data = json.loads(
        local_norm
    )

    local_fingerprint = sha256_text(
        local_norm
    )

    external_repo = None

    try:
        external_repo = run_fresh_clone()

        target = os.environ.get(
            "GITHUB_SHA"
        )

        if target:
            subprocess.run(
                [
                    "git",
                    "checkout",
                    target,
                ],
                cwd=external_repo,
                check=True,
            )
        else:
            print(
                "⚠️ GITHUB_SHA unavailable; "
                "using cloned repository HEAD."
            )

        external_raw = run_pipeline(
            external_repo
        )

        external_norm = normalize_report(
            external_raw
        )

        external_data = json.loads(
            external_norm
        )

        external_fingerprint = sha256_text(
            external_norm
        )

        local_required = (
            extract_required_structure(
                local_data
            )
        )

        external_required = (
            extract_required_structure(
                external_data
            )
        )

        structure_match = (
            local_required
            ==
            external_required
        )

        fingerprint_match = (
            local_fingerprint
            ==
            external_fingerprint
        )

        print(
            "LOCAL FINGERPRINT:",
            local_fingerprint
        )

        print(
            "EXTERNAL FINGERPRINT:",
            external_fingerprint
        )

        print(
            "STRUCTURE MATCH:",
            structure_match
        )

        print(
            "FINGERPRINT MATCH:",
            fingerprint_match
        )

        independent_replay_verified = bool(
            structure_match
            and fingerprint_match
        )

        artifact = {
            "independent_replay_verified":
                independent_replay_verified,

            "fingerprint_match":
                fingerprint_match,

            "structure_match":
                structure_match,

            "local_fingerprint":
                local_fingerprint,

            "external_fingerprint":
                external_fingerprint,

            "comparison_method":
                "normalized_full_canonical_report",

            "normalization_precision":
                8,

            "volatile_keys_removed":
                sorted(VOLATILE_KEYS),

            "scientific_role":
                "independent_reproducibility_gate",

            "status": (
                "verified"
                if independent_replay_verified
                else "failed"
            ),
        }

        os.makedirs(
            "artifacts",
            exist_ok=True
        )

        with open(
            "artifacts/external_replay_verification.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                artifact,
                f,
                indent=2,
                sort_keys=True,
            )

        if not independent_replay_verified:
            print(
                "❌ INDEPENDENT REPRODUCTION FAILED"
            )
            return False

        print(
            "✅ INDEPENDENT REPRODUCTION VERIFIED"
        )

        return True

    finally:
        if external_repo:
            shutil.rmtree(
                external_repo,
                ignore_errors=True,
            )

if __name__ == "__main__":
    ok = compare()
    if not ok:
        raise SystemExit(1)
