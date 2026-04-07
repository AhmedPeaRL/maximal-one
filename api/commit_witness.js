// commit_witness.js
// SAFE bridge: UI → Secure backend → GitHub

export async function commitWitness(entry) {
  try {
    const payload = {
      timestamp: Date.now(),
      entry
    };

    // 🔐 call YOUR secure backend instead of GitHub directly
    const response = await fetch("/api/witness", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error("Commit failed");
    }

    return true;

  } catch (e) {
    console.error("Commit error:", e);
    return false;
  }
}
