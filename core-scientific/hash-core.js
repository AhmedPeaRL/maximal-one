import crypto from "crypto";

export function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

export function computeDeterministicArtifactHash(scientificHash, compositeSeal) {
  return sha256(scientificHash + compositeSeal);
}
