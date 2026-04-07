// witness_persistence.js
// deterministic witness recorder (local layer)

export function persistWitness(entry) {
  try {
    const existing = JSON.parse(localStorage.getItem("witness_log") || "[]");

    const updated = [
      ...existing,
      {
        timestamp: Date.now(),
        ...entry
      }
    ];

    localStorage.setItem("witness_log", JSON.stringify(updated.slice(-50)));

  } catch (e) {
    console.warn("Persistence failed", e);
  }
}
