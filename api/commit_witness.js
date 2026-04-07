export async function commitWitness(entry) {
  try {
    const payload = {
      timestamp: Date.now(),
      entry
    };

    const response = await fetch("/api/witness", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-witness-key": "public-gateway"
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
