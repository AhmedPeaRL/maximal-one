export async function loadLiveWitness() {
  try {
    const res = await fetch('/maximal-one/artifacts/canonical_report.json', {
      cache: "no-store"
    });

    if (!res.ok) throw new Error("No report");

    const data = await res.json();

    return {
      alpha: data?.spectral_profile?.estimated_alpha ?? "N/A",
      std: data?.spectral_profile?.bootstrap_std ?? "N/A",
      valid: true
    };

  } catch (e) {
    return {
      alpha: "N/A",
      std: "N/A",
      valid: false
    };
  }
}
