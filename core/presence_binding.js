export async function bindPresence() {
  try {
    const [reportRes, decisionRes, stateRes] = await Promise.all([
      fetch('./artifacts/canonical_report.json', { cache: "no-store" }),
      fetch('./artifacts/decision.json', { cache: "no-store" }),
      fetch('./data/latest_state.json', { cache: "no-store" })
    ]);

    const report = reportRes.ok ? await reportRes.json() : null;
    const decision = decisionRes.ok ? await decisionRes.json() : null;
    const state = stateRes.ok ? await stateRes.json() : null;

    return {
      alpha: report?.spectral_profile?.estimated_alpha ?? null,
      sigma: report?.spectral_profile?.bootstrap_std ?? null,
      decision: decision?.decision ?? "unknown",
      layer: state?.layer ?? "unknown",
      field: state?.field ?? "unknown",
      timestamp: Date.now()
    };

  } catch (e) {
    return {
      error: true,
      timestamp: Date.now()
    };
  }
}
