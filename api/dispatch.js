export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ ok: false });
  }

  try {
    const { input } = req.body;

    if (!input || typeof input !== "string") {
      return res.status(400).json({ ok: false, error: "invalid input" });
    }

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
            timestamp: Date.now()
          }
        })
      }
    );

    if (!response.ok) {
      return res.status(500).json({ ok: false });
    }

    return res.json({ ok: true });

  } catch (e) {
    return res.status(500).json({ ok: false, error: e.message });
  }
        }
