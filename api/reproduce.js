export async function onRequestPost(context) {
  try {
    const payload = {
      event_type: "external_reproduction",
      client_payload: {
        trigger: "manual",
        timestamp: Date.now()
      }
    };

    const res = await fetch(
      `https://api.github.com/repos/${context.env.GH_REPO}/dispatches`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${context.env.GH_TOKEN}`,
          "Accept": "application/vnd.github+json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }
    );

    return new Response(JSON.stringify({ ok: res.ok }), { status: 200 });

  } catch (e) {
    return new Response(JSON.stringify({ ok: false }), { status: 500 });
  }
}
export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ ok: false });
  }

  try {
    const payload = {
      timestamp: Date.now(),
      source: "external_reproduction_request",
      repo: "AhmedPeaRL/maximal-one"
    };

    // Trigger PUBLIC reproducibility via GitHub Actions
    const response = await fetch(
      "https://api.github.com/repos/AhmedPeaRL/maximal-one/dispatches",
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.GH_TOKEN}`,
          "Accept": "application/vnd.github+json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          event_type: "external_reproduction",
          client_payload: payload
        })
      }
    );

    if (!response.ok) {
      return res.status(500).json({ ok: false });
    }

    return res.json({ ok: true, message: "Reproduction triggered" });

  } catch (e) {
    return res.status(500).json({ ok: false });
  }
}
