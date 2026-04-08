// ⚠️ ZERO-TRUST SECURE BRIDGE
// No secrets exposed to frontend

export async function sendWitnessSecure(envelope) {
  try {
    const response = await fetch("https://api.github.com/repos/ahmedpearl/maximal-one/dispatches", {
      method: "POST",
      headers: {
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",

        // ⚠️ NEVER PUT TOKEN HERE IN REAL SYSTEM
        // This must be proxied through a backend or serverless function
        "Authorization": `Bearer ${getEphemeralToken()}`
      },
      body: JSON.stringify({
        event_type: "external_witness",
        client_payload: envelope
      })
    });

    if (!response.ok) {
      throw new Error("Dispatch failed: " + response.status);
    }

    return true;

  } catch (err) {
    console.error("Secure witness error:", err);
    throw err;
  }
}

// ⚠️ TEMP placeholder — MUST be replaced
function getEphemeralToken() {
  throw new Error("No token allowed in frontend. Use backend proxy.");
      }
