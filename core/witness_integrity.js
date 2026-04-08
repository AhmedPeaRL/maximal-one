import crypto from "crypto";

export function buildWitnessEnvelope(input) {
  const timestamp = new Date().toISOString();

  const payload = {
    input,
    timestamp
  };

  const serialized = JSON.stringify(payload);

  const hash = crypto
    .createHash("sha256")
    .update(serialized)
    .digest("hex");

  return {
    payload,
    hash
  };
}
