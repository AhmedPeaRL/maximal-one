export async function loadRealitySnapshot() {
  try {
    const [reportRes, extRes] = await Promise.all([
      fetch('./artifacts/canonical_report.json', { cache: "no-store" }),
      fetch('./artifacts/external_validation.json', { cache: "no-store" })
    ]);

    const report = await reportRes.json();
    const ext = await extRes.json();

    return {
      alpha: report?.spectral_profile?.estimated_alpha ?? null,
      std: report?.spectral_profile?.bootstrap_std ?? null,
      external_status: ext?.status ?? "unknown",
      hash: ext?.proof?.hash ?? null
    };

  } catch (e) {
    return {
      alpha: null,
      std: null,
      external_status: "error",
      hash: null
    };
  }
}
