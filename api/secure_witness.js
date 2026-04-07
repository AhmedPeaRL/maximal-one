export async function sendWitnessSecure(payload) {
  const response = await fetch("https://api.github.com/repos/AhmedPeaRL/maximal-one/dispatches", {
    method: "POST",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${import.meta.env.VITE_GITHUB_TOKEN}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      event_type: "external_witness",
      client_payload: payload
    })
  });

  if (!response.ok) {
    throw new Error("Failed to send witness");
  }

  return true;
}
