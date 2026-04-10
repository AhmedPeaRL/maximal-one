import crypto from "crypto";

const RATE_LIMIT = 10; // max requests
const WINDOW_MS = 60000; // 1 min

const memory = new Map();

function rateLimit(ip) {
  const now = Date.now();
  if (!memory.has(ip)) {
    memory.set(ip, []);
  }

  const timestamps = memory.get(ip).filter(t => now - t < WINDOW_MS);

  if (timestamps.length >= RATE_LIMIT) {
    return false;
  }

  timestamps.push(now);
  memory.set(ip, timestamps);
  return true;
}

function generateSignature(payload) {
  return crypto
    .createHash("sha256")
    .update(JSON.stringify(payload))
    .digest("hex");
}

export default async function handler(req, res) {

  if (req.method !== "POST") {
    return res.status(405).json({ ok: false });
  }

  try {
    const { input } = req.body;

    if (!input || typeof input !== "string") {
      return res.status(400).json({ ok: false });
    }

    if (input.length > 500) {
      return res.status(400).json({ ok: false });
    }

    const ip = req.headers["x-forwarded-for"] || "unknown";

    // 🔴 rate limiting
    if (!rateLimit(ip)) {
      return res.status(429).json({ ok: false, error: "rate limit exceeded" });
    }

    const payload = {
      input,
      ip,
      timestamp: Date.now()
    };

    // 🔴 anti-replay hash
    const signature = generateSignature(payload);

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
            ...payload,
            signature
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
