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
      timestamp: Date.now()
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

  score += Math.random() * 0.2;

  return Math.min(score, 1);
}
