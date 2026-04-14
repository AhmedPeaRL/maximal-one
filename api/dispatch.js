import crypto from "crypto";

const ALLOWED_ORIGIN = "https://ahmedpearl.github.io";
const STRICT_PATH = "/maximal-one";

const RATE_LIMIT = 10;
const WINDOW_MS = 60000;

const memory = new Map();

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

function isValidInput(input) {
  if (typeof input !== "string") return false;

  // طول منطقي
  if (input.length === 0 || input.length > 500) return false;

  // منع payloads الخطيرة بس
  const forbiddenPatterns = [
    /<script/i,
    /<\/script>/i,
    /javascript:/i,
    /onerror=/i,
    /onload=/i
  ];

  for (const pattern of forbiddenPatterns) {
    if (pattern.test(input)) return false;
  }

  return true;
}

export default async function handler(req, res) {
  const origin = req.headers.origin || "";

  if (!origin.startsWith(ALLOWED_ORIGIN)) {
    return res.status(403).json({ ok: false, error: "forbidden origin" });
  }

  const referer = req.headers.referer || "";

  if (!referer.includes(STRICT_PATH)) {
    return res.status(403).json({ ok: false, error: "invalid path" });
  }
  
  if (req.method !== "POST") {
    return res.status(405).json({ ok: false });
  }

  try {
    const { input } = req.body;

    if (!isValidInput(input)) {
      return res.status(400).json({ ok: false, error: "invalid input" });
    }

    const ip = req.headers["x-forwarded-for"] || req.socket.remoteAddress || "unknown";

    // 🔥 ACTIVATE RATE LIMIT
    if (!rateLimit(ip)) {
      return res.status(429).json({ ok: false, error: "rate limit exceeded" });
    }

function safeCompare(a, b) {
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);

  if (bufA.length !== bufB.length) return false;

  return crypto.timingSafeEqual(bufA, bufB);
}

    const pulse = Math.floor(Date.now() / 5000);

    const nonce = crypto.randomBytes(16).toString("hex");
    
    const payload = {
      input,
      pulse,
      nonce,
      timestamp: Date.now()
    };

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
      return res.status(500).json({ ok: false });
    }

    return res.json({ ok: true });

  } catch {
    return res.status(500).json({ ok: false });
  }
}
