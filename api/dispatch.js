// SECURE SERVERLESS PROXY
// This runs on server (NOT frontend)

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const body = req.body;

    if (!body || typeof body !== "object") {
      return res.status(400).json({ error: "Invalid payload" });
    }

    // basic size guard
    const size = JSON.stringify(body).length;
    if (size > 5000) {
      return res.status(400).json({ error: "Payload too large" });
    }

    const response = await fetch(
      "https://api.github.com/repos/ahmedpearl/maximal-one/dispatches",
      {
        method: "POST",
        headers: {
          "Accept": "application/vnd.github+json",
          "Authorization": `Bearer ${process.env.GITHUB_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          event_type: "external_witness",
          client_payload: body
        })
      }
    );

    if (!response.ok) {
      return res.status(500).json({ error: "Dispatch failed" });
    }

    return res.status(200).json({ status: "ok" });

  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
