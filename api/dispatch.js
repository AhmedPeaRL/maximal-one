import crypto from "crypto";

const ALLOWED_ORIGIN = "https://ahmedpearl.github.io";
const STRICT_PATH = "/maximal-one";

const RATE_LIMIT = 10;
const WINDOW_MS = 60000;

const memory = new Map();
const used = new Set();

export function preventReplay(signature) {
  if (used.has(signature)) {
    return false;
  }

  used.add(signature);

  setTimeout(() => {
    used.delete(signature);
  }, 60000);

  return true;
}

function rateLimit(ip) {
  const now = Date.now();
  if (!memory.has(ip)) memory.set(ip, []);

  const timestamps = memory.get(ip).filter(t => now - t < WINDOW_MS);

  if (timestamps.length >= RATE_LIMIT) return false;

  timestamps.push(now);
  memory.set(ip, timestamps);
  return true;
}

function canonicalStringify(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort());
}

function generateSignature(payload) {
  return crypto
    .createHmac("sha256", process.env.WITNESS_SECRET)
    .update(canonicalStringify(payload))
    .digest("hex");
}

function safeCompare(a, b) {
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);

  if (bufA.length !== bufB.length) return false;
  return crypto.timingSafeEqual(bufA, bufB);
}

function isValidInput(input) {
  if (typeof input !== "string") return false;
  if (input.length === 0 || input.length > 500) return false;

  const forbidden = [
    /<script/i,
    /javascript:/i,
    /onerror=/i,
    /onload=/i
  ];

  return !forbidden.some(p => p.test(input));
}

export default async function handler(req, res) {
  const origin = req.headers.origin || "";

  try {
    const parsed = new URL(origin);
    if (parsed.origin !== ALLOWED_ORIGIN) {
      return res.status(403).json({ ok: false, error: "forbidden origin" });
    }
  } catch {
    return res.status(403).json({ ok: false });
  }

  if (req.method !== "POST") {
    return res.status(405).json({ ok: false });
  }

  try {
    const { input, signature } = req.body;

    if (!isValidInput(input)) {
      return res.status(400).json({ ok: false, error: "invalid input" });
    }

    const ip =
      (req.headers["x-forwarded-for"] || "").split(",")[0].trim() ||
      req.socket.remoteAddress ||
      "unknown";

    if (!rateLimit(ip)) {
      return res.status(429).json({ ok: false, error: "rate limit exceeded" });
    }

    const pulse = Math.floor(Date.now() / 5000);

    const payload = {
      input,
      pulse
    };

    const expected = generateSignature(payload);

    if (!safeCompare(signature || "", expected)) {
      return res.status(403).json({ ok: false, error: "invalid signature" });
    }

    const gh = await fetch(
      "https://api.github.com/repos/ahmedpearl/maximal-one/dispatches",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.GH_TOKEN}`,
          Accept: "application/vnd.github+json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          event_type: "external_witness",
          client_payload: payload
        })
      }
    );

    if (!gh.ok) {
      return res.status(500).json({ ok: false });
    }

    return res.json({ ok: true });

  } catch (e) {
    return res.status(500).json({ ok: false, error: e.message });
  }
}
