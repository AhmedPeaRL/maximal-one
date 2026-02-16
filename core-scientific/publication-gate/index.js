import fs from "fs";
import crypto from "crypto";
import { computeDeterministicArtifactHash } from "../hash-core.js";

function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

function writeCanonicalJSON(path, obj) {
  const ordered = Object.keys(obj)
    .sort()
    .reduce((acc, key) => {
      acc[key] = obj[key];
      return acc;
    }, {});

  const json = JSON.stringify(ordered, null, 2) + "\n";
  fs.writeFileSync(path, json, { encoding: "utf8" });
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

  writeCanonicalJSON(
    "./core-scientific/publication-gate/report.json",
    report
  );

  console.log("Scientific hash:", scientificHash);
  console.log("Composite seal:", compositeSeal);
  console.log("Deterministic artifact hash:", deterministicArtifactHash);
}

main();
