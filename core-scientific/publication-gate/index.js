import fs from "fs";
import crypto from "crypto";
import { computeDeterministicArtifactHash } from "../hash-core.js";

function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

function main() {

  const scientificPayload = "MAXIMAL_ONE_SCIENTIFIC_CORE_V1";
  const scientificHash = sha256(scientificPayload);

  const compositePayload = scientificHash + "::MAXIMAL_SEAL_V1";
  const compositeSeal = sha256(compositePayload);

  const deterministicArtifactHash =
    computeDeterministicArtifactHash(
      scientificHash,
      compositeSeal
    );

  const report = {
    scientificHash,
    compositeSeal,
    deterministicArtifactHash
  };

  fs.writeFileSync(
    "./core-scientific/publication-gate/report.json",
    JSON.stringify(report, null, 2)
  );

  console.log("Scientific hash:", scientificHash);
  console.log("Composite seal:", compositeSeal);
  console.log("Deterministic artifact hash:", deterministicArtifactHash);
}

main();
