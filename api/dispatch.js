export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).end();
  }

  const { input } = req.body;

  const gh = await fetch("https://api.github.com/repos/ahmedpearl/maximal-one/dispatches", {
    method: "POST",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${process.env.GH_TOKEN}`,
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

  if (!gh.ok) {
    return res.status(500).json({ error: "dispatch failed" });
  }

  return res.status(200).json({ ok: true });
}
