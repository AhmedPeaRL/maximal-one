import crypto from "crypto";

const ALLOWED_ORIGIN = "https://ahmedpearl.github.io";
const STRICT_PATH = "/maximal-one";

function canonicalStringify(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort());
}

function generateChallengeID(payload) {
  return crypto
    .createHash("sha256")
    .update(canonicalStringify(payload) + Date.now())
    .digest("hex");
}

function isValidChallenge(input) {
  if (typeof input !== "string") return false;
  if (input.length === 0 || input.length > 1000) return false;

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
      return res.status(403).json({ ok: false });
    }
  } catch {
    return res.status(403).json({ ok: false });
  }

  if (req.method !== "POST") {
    return res.status(405).json({ ok: false });
  }

  try {
    const { challenge } = req.body;

    if (!isValidChallenge(challenge)) {
      return res.status(400).json({ ok: false });
    }

    const payload = {
      challenge,
      timestamp: Date.now(),
      type: "external_challenge"
    };

    const id = generateChallengeID(payload);

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
          event_type: "external_reproduction",
          client_payload: {
            ...payload,
            challenge_id: id
          }
        })
      }
    );

    if (!response.ok) {
      return res.status(500).json({ ok: false });
    }

    return res.json({ ok: true, challenge_id: id });

  } catch {
    return res.status(500).json({ ok: false });
  }
}
