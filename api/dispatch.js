export default async function handler(req, res) {

  if (req.method !== "POST") {
    return res.status(405).json({ ok: false });
  }

  try {
    const { input } = req.body;

    // 1. strict validation
    if (!input || typeof input !== "string") {
      return res.status(400).json({ ok: false, error: "invalid input" });
    }

    if (input.length > 500) {
      return res.status(400).json({ ok: false, error: "input too large" });
    }

    // 2. basic abuse protection
    const ip = req.headers["x-forwarded-for"] || "unknown";

    // (اختياري لاحقاً: تخزين IP + rate limiting)

    // 3. dispatch to GitHub
    const response = await fetch(
      "https://api.github.com/repos/ahmedpearl/maximal-one/dispatches",
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.GH_TOKEN}`,
          "Accept": "application/vnd.github+json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          event_type: "external_witness",
          client_payload: {
            input,
            ip,
            timestamp: Date.now()
          }
        })
      }
    );

    if (!response.ok) {
      const text = await response.text();
      return res.status(500).json({ ok: false, error: text });
    }

    return res.json({ ok: true });

  } catch (e) {
    return res.status(500).json({ ok: false, error: e.message });
  }
}
