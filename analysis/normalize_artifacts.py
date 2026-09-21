import json
from pathlib import Path

ARTIFACTS = Path("artifacts")

for path in sorted(ARTIFACTS.glob("*.json")):
    try:
        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        # ------------------------------------------------------------
        # SEALED CANONICAL REPORT PROTECTION
        #
        # Once canonical_report.json is sealed, its raw bytes become
        # part of the cryptographic provenance chain through:
        #
        #   artifacts/report.hash
        #   artifacts/witness_lock.json
        #   artifacts/reproducibility_stamp.json
        #
        # Therefore no later normalization step may rewrite it.
        #
        # Semantic JSON equality is not sufficient here because the
        # integrity layer intentionally protects the exact bytes.
        # ------------------------------------------------------------

        if (
            path.name == "canonical_report.json"
            and data.get("_sealed") is True
        ):
            print(
                "🔒 SEALED canonical_report.json preserved byte-for-byte"
            )
            continue

        path.write_text(
            json.dumps(
                data,
                indent=2,
                sort_keys=True
            ) + "\n",
            encoding="utf-8"
        )

    except Exception:
        # Preserve the historical behavior for non-JSON or malformed
        # artifacts: normalization is best-effort and must not destroy
        # the original artifact.
        pass

print("✅ ARTIFACT NORMALIZATION COMPLETE")
