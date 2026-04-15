import crypto from "crypto";

export async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const body = req.body;

    if (!body || typeof body !== "object") {
      return res.status(400).json({ error: "Invalid payload" });
    }

    const raw = JSON.stringify(body);

    if (raw.length > 5000) {
      return res.status(413).json({ error: "Payload too large" });
    }

    // Hash فقط — بدون ثقة مسبقة
    const hash = crypto
      .createHash("sha256")
      .update(raw)
      .digest("hex");

    // forward → GitHub dispatch
    const gh = await fetch(
      "https://api.github.com/repos/AhmedPeaRL/maximal-one/dispatches",
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.GH_TOKEN}`,
          "Accept": "application/vnd.github+json"
        },
        body: JSON.stringify({
          event_type: "external_witness",
          client_payload: {
            raw,
            hash,
            timestamp: Date.now()
          }
        })
      }
    );

    if (!gh.ok) {
      return res.status(500).json({ error: "Dispatch failed" });
    }

    return res.json({
      ok: true,
      hash,
      message: "Witness propagated"
    });

  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
}
