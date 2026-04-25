export function simulateTrade(decision) {
  const price = Math.random() * 100; // placeholder
  const pnl = (Math.random() - 0.5) * 2;

  if (!decision || !decision.action) {
    return { ok: false, error: "No decision" };
  }

  return {
    action: decision.action,
    price,
    pnl,
    timestamp: Date.now()
  };
}

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
