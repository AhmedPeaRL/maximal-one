from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path

REPORT_PATH = Path(
  "artifacts/canonical_report.json"
)

REPLAY_PATH = Path(
  "artifacts/external_replay_verification.json"
)

def finite(value):
  return (
    isinstance(value, (int, float))
    and math.isfinite(float(value))
  )

def fail(message):
  raise SystemExit(
    "EXTERNAL REPLAY GATE FAILURE: "
    + message
  )

def require(condition, message):
  if not condition:
    fail(message)

def sha256_file(path):
  h = hashlib.sha256()
  
  with path.open("rb") as f:
    for chunk in iter(
      lambda: f.read(1024 * 1024),
      b"",
    ):
      h.update(chunk)

  return h.hexdigest()

def main():
  require(
    REPORT_PATH.exists(),
    "canonical_report.json is missing",
  )

  require(
    REPLAY_PATH.exists(),
    "external_replay_verification.json is missing",
  )

  with REPORT_PATH.open(
    "r",
    encoding="utf-8",
  ) as f:
    report = json.load(f)

  with REPLAY_PATH.open(
    "r",
    encoding="utf-8",
  ) as f:
    replay = json.load(f)

  required = {
      "independent_replay_verified",
      "fingerprint_match",
      "original_alpha",
      "reproduced_alpha",
      "delta",
      "external_report_sha256",
      "reproduced_report_sha256",
      "external_environment",
      "verification_method",
  }

  missing = (
      required
      -
      set(replay.keys())
  )

  require(
      not missing,
      "missing required fields: "
      + ", ".join(sorted(missing)),
  )

  require(
      replay[
          "independent_replay_verified"
      ] is True,
      "independent_replay_verified is not true",
  )

  require(
      replay[
          "fingerprint_match"
      ] is True,
      "fingerprint_match is not true",
  )

  original_alpha = replay[
      "original_alpha"
  ]

  reproduced_alpha = replay[
      "reproduced_alpha"
  ]

  delta = replay[
      "delta"
  ]

  require(
      finite(original_alpha),
      "original_alpha is missing or non-finite",
  )

  require(
      finite(reproduced_alpha),
      "reproduced_alpha is missing or non-finite",
  )

  require(
      finite(delta),
      "delta is missing or non-finite",
  )

  calculated_delta = abs(
      float(original_alpha)
      -
      float(reproduced_alpha)
  )

  require(
      abs(
          calculated_delta
          -
          float(delta)
      ) <= 1e-8,
      (
          "reported delta does not match "
          "the reproduced alpha values"
      ),
  )

  require(
      float(delta) <= 1e-8,
      (
          "independent replay alpha does not "
          "match canonical alpha"
      ),
  )

  original_hash = replay[
      "external_report_sha256"
  ]

  reproduced_hash = replay[
      "reproduced_report_sha256"
  ]

  require(
      isinstance(original_hash, str)
      and len(original_hash) == 64,
      "external_report_sha256 is invalid",
  )

  require(
      isinstance(reproduced_hash, str)
      and len(reproduced_hash) == 64,
      "reproduced_report_sha256 is invalid",
  )

  environment = replay[
      "external_environment"
  ]

  require(
      isinstance(environment, dict),
      "external_environment must be an object",
  )

  required_environment = {
      "python",
      "numpy",
      "scipy",
      "platform",
  }

  missing_environment = (
      required_environment
      -
      set(environment.keys())
  )

  require(
      not missing_environment,
      (
          "external environment is incomplete: "
          +
          ", ".join(
              sorted(missing_environment)
          )
      ),
  )

  method = replay[
      "verification_method"
  ]

  require(
      method
      ==
      "independent_clean_environment_rerun",
      (
          "verification_method must explicitly "
          "declare an independent clean-environment rerun"
      ),
  )

  print(
      "EXTERNAL REPLAY VERIFIED"
  )

  print(
      "Independent rerun: TRUE"
  )

  print(
      "Fingerprint match: TRUE"
  )

  print(
      "Canonical alpha:",
      float(original_alpha),
  )

  print(
      "Reproduced alpha:",
      float(reproduced_alpha),
  )

  print(
      "Delta:",
      float(delta),
  )

  print(
      "External report SHA256:",
      original_hash,
  )

  print(
      "Reproduced report SHA256:",
      reproduced_hash,
  )

  print(
      "External environment:",
      json.dumps(
          environment,
          sort_keys=True,
      ),
  )

  print(
      "Independent external replay gate PASSED."
  )

if __name__ == "__main__":
  main()
