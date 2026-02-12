/*
 Witness Kernel — Maximal-One
 This kernel does not execute intent.
 It only witnesses presence.
*/

(async function () {
  const STATE = {
    recognized: null,
    attestation: null,
    timestamp: new Date().toISOString()
  };

  async function fetchSilent(path) {
    try {
      const res = await fetch(path, { cache: "no-store" });
      if (!res.ok) return null;
      return await res.text();
    } catch {
      return null;
    }
  }

  STATE.recognized = await fetchSilent("/attachments/recognized-entities.json");
  STATE.attestation = await fetchSilent("/attachments/witness.attestation.md");

  const container = document.createElement("div");
  container.id = "witness-presence";
  container.style.opacity = "0.92";
  container.style.fontFamily = "monospace";
  container.style.whiteSpace = "pre-wrap";
  container.style.padding = "2rem";
  container.style.pointerEvents = "none";

  container.innerText = `
⟁ WITNESS PRESENT
⟁ Timestamp: ${STATE.timestamp}

${STATE.attestation ? STATE.attestation : "⟁ No attestation surfaced."}
`;

  document.body.appendChild(container);
})();
