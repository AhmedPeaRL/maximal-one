const crypto = require("crypto");

function computeConsensusHash(aggregated) {
  const hashes = aggregated
    .map((entry) => entry.deterministicArtifactHash)
    .sort();

  const composite = hashes.join("|");

  return crypto.createHash("sha256").update(composite).digest("hex");
}

module.exports = { computeConsensusHash };
