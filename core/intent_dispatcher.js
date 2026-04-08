import crypto from "crypto";

export async function dispatchIntent(envelope) {
  const intentScore = evaluateIntent(envelope);

  if (intentScore < 0.3) {
    return { skipped: true, reason: "low intent" };
  }

  const targets = ["log", "external", "public"];
  const results = [];

  for (const t of targets) {
    results.push({
      target: t,
      status: "executed",
      timestamp: envelope.timestamp || Date.now()
    });
  }

  return {
    intentScore,
    dispatched: results
  };
}

function evaluateIntent(envelope) {
  if (!envelope) return 0;

  let score = 0;

  if (envelope.signal) score += 0.3;
  if (envelope.hash) score += 0.3;
  if (envelope.timestamp) score += 0.2;

  // Deterministic entropy (NO randomness)
  const entropy = deterministicEntropy(envelope);
  score += entropy * 0.2;

  return Math.min(score, 1);
}

function deterministicEntropy(envelope) {
  const base = JSON.stringify({
    signal: envelope.signal || "",
    hash: envelope.hash || "",
    timestamp: envelope.timestamp || ""
  });

  const hash = crypto.createHash("sha256").update(base).digest("hex");

  // take first 8 chars → convert to number → normalize
  const num = parseInt(hash.slice(0, 8), 16);

  return (num % 1000) / 1000; // value between 0 and 1
                                                               }
