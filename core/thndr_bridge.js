export async function executeThndrBridge(decision) {
  if (decision.confidence < 0.8) {
    return { ok: false, error: "low confidence" };
  }
  
  if (!decision || !decision.action) {
    return { ok: false, error: "No decision" };
  }

  const payload = {
    action: decision.action,
    asset: decision.asset,
    confidence: decision.confidence,
    timestamp: new Date().toISOString()
  };

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
