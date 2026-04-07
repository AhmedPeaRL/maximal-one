export default async function handler(req, res) {
  try {
    const payload = req.body;

    const SECRET = process.env.WITNESS_SECRET;

    if (req.headers["x-witness-key"] !== SECRET) {
      return res.status(403).json({ error: "Unauthorized" });
    }

    const response = await fetch("https://api.github.com/repos/ahmedpearl/maximal-one/dispatches", {
      method: "POST",
      headers: {
        "Accept": "application/vnd.github+json",
        "Authorization": `Bearer ${process.env.GITHUB_TOKEN}`,
        "Content-Type": "application/json",
        "x-witness-key": "Token"
      },
      body: JSON.stringify({
        event_type: "external_witness",
        client_payload: payload
      })
    });

    if (!response.ok) {
      return res.status(500).json({ error: "GitHub dispatch failed" });
    }

    return res.status(200).json({ ok: true });

  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
}
