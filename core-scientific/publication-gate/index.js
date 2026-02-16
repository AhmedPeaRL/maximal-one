import fs from "fs";
import crypto from "crypto";
import { computeDeterministicArtifactHash } from "../hash-core.js";

function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

function main() {

  // 1️⃣ احسب scientific hash
  const scientificPayload = "MAXIMAL_ONE_SCIENTIFIC_CORE_V1";
  const scientificHash = sha256(scientificPayload);

  // 2️⃣ احسب composite seal
  const compositePayload = scientificHash + "::MAXIMAL_SEAL_V1";
  const compositeSeal = sha256(compositePayload);

  // 3️⃣ احسب deterministic artifact hash
  const deterministicArtifactHash =
    computeDeterministicArtifactHash(
      scientificHash,
      compositeSeal
    );

  const report = {
    scientificHash,
    compositeSeal,
    deterministicArtifactHash,
    timestamp: new Date().toISOString()
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
