import fs from "fs";
import crypto from "crypto";
import { computeDeterministicArtifactHash } from "../hash-core.js";

function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

function verify() {

  const scientificPayload = "MAXIMAL_ONE_SCIENTIFIC_CORE_V1";
  const expectedScientificHash = sha256(scientificPayload);

  const compositePayload =
    expectedScientificHash + "::MAXIMAL_SEAL_V1";

  const expectedCompositeSeal =
    sha256(compositePayload);

  const expectedDeterministicArtifactHash =
    computeDeterministicArtifactHash(
      expectedScientificHash,
      expectedCompositeSeal
    );

  const raw = fs.readFileSync(
    "./core-scientific/publication-gate/report.json",
    "utf8"
  );

  const report = JSON.parse(raw);

  if (
    report.scientificHash !== expectedScientificHash ||
    report.compositeSeal !== expectedCompositeSeal ||
    report.deterministicArtifactHash !==
      expectedDeterministicArtifactHash
  ) {
    throw new Error("Report integrity mismatch");
  }

  console.log("Report integrity verified.");
}

verify();
