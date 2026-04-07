// commit_witness.js
// real system bridge: UI → GitHub → Pipeline

export async function commitWitness(entry) {
  try {
    const payload = {
      timestamp: Date.now(),
      entry
    };

    // GitHub API endpoint (replace with your repo)
    const response = await fetch("https://api.github.com/repos/ahmedpearl/maximal-one/dispatches", {
      method: "POST",
      headers: {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer YOUR_GITHUB_TOKEN",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        event_type: "external_witness",
        client_payload: payload
      })
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
