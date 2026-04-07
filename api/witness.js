export default async function handler(req, res) {
  try {
    if (req.method !== "POST") {
      return res.status(405).json({ error: "Method not allowed" });
    }

    const SECRET = process.env.WITNESS_SECRET;
    const TOKEN = process.env.GITHUB_TOKEN;

    const incomingKey = req.headers["x-witness-key"];
    if (!incomingKey || incomingKey !== SECRET) {
      return res.status(403).json({ error: "Unauthorized" });
    }

    const payload = req.body;

    // 🧠 Replay protection
    if (!payload.timestamp || !payload.entry) {
      return res.status(400).json({ error: "Malformed payload" });
    }

    const now = Date.now();
    const drift = Math.abs(now - payload.timestamp);

    if (drift > 1000 * 60 * 5) {
      return res.status(400).json({ error: "Stale payload rejected" });
    }

    // 🔒 Forward to GitHub
    const gh = await fetch(
      "https://api.github.com/repos/ahmedpearl/maximal-one/dispatches",
      {
        method: "POST",
        headers: {
          "Accept": "application/vnd.github+json",
          "Authorization": `Bearer ${TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          event_type: "external_witness",
          client_payload: payload
        })
      }
    );

    if (!gh.ok) {
      return res.status(500).json({ error: "GitHub dispatch failed" });
    }

    return res.status(200).json({ ok: true });

  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
}
