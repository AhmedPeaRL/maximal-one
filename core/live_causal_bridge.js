export async function sendWitnessToSystem(input) {
  try {
    const res = await fetch("https://api.github.com/repos/ahmedpearl/maximal-one/dispatches", {
      method: "POST",
      headers: {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer YOUR_GITHUB_TOKEN",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        event_type: "external_witness",
        client_payload: {
          input,
          timestamp: new Date().toISOString()
        }
      })
    });

    if (!res.ok) {
      throw new Error("Dispatch failed");
    }

    return { status: "sent" };

  } catch (e) {
    return { status: "error", error: e.message };
  }
}
