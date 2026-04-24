export async function resolveState() {
  try {
    const verdict = await fetch('/api/state').then(r => r.json());
    const artifact = await fetch('./public/artifact.json').then(r => r.json());

    return {
      field: verdict.passed ? "stable" : "probing",
      layer: verdict.layer || "present",
      event: artifact
    };

  } catch (e) {
    return {
      field: "degraded",
      layer: "fallback",
      event: null
    };
  }
}
