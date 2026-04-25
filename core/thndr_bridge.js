// deterministic trade simulation (NO randomness)

function deterministicHash(str) {
  let hash = 0;

  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }

  return Math.abs(hash);
}

function deriveValue(seed, min, max) {
  const normalized = (seed % 1000) / 1000;
  return min + (max - min) * normalized;
}

export function simulateTrade(decision) {
  if (!decision || !decision.action) {
    return { ok: false, error: "No decision" };
  }

  const seed = deterministicHash(JSON.stringify(decision));

  const price = deriveValue(seed, 10, 100);
  const pnl = deriveValue(seed + 42, -1, 1);

  return {
    action: decision.action,
    price,
    pnl,
    timestamp: Date.now(),
    deterministic: true
  };
}

export async function executeThndrBridge(payload) {
  try {
    const res = await fetch("/api/thndr-dispatch", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const r = await res.json();

    return r;

  } catch (e) {
    return { ok: false, error: e.message };
  }
}
