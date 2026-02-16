import fs from "fs";
import { computeDeterministicArtifactHash } from "../hash-core.js";

function audit() {

  const report = JSON.parse(
    fs.readFileSync("./core-scientific/publication-gate/report.json")
  );

  const recomputed =
    computeDeterministicArtifactHash(
      report.scientificHash,
      report.compositeSeal
    );

  if (recomputed !== report.deterministicArtifactHash) {
    console.error("AUDIT FAILURE: Deterministic artifact hash mismatch");
    process.exit(1);
  }

  console.log("AUDIT SUCCESS: Deterministic artifact hash verified independently.");
}

audit();
