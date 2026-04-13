const fs = require('fs');
const crypto = require('crypto');

const raw = fs.readFileSync('payload.json', 'utf8');
const data = JSON.parse(raw);

const secret = process.env.WITNESS_SECRET;

if (!secret) {
  console.log("No secret — skipping verification");
  process.exit(0);
}

const { signature, ...payloadWithoutSig } = data;

if (!signature) {
  console.error("Missing signature");
  process.exit(1);
}

const canonical = JSON.stringify(payloadWithoutSig, Object.keys(payloadWithoutSig).sort());

const expected = crypto
  .createHmac('sha256', secret)
  .update(canonical)
  .digest('hex');

function safeCompare(a, b) {
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);

  if (bufA.length !== bufB.length) return false;
  return crypto.timingSafeEqual(bufA, bufB);
}

if (!safeCompare(signature, expected)) {
  console.error("Invalid signature (HMAC mismatch)");
  process.exit(1);
}

const { execSync } = require('child_process');

try {
  execSync(`python analysis/replay_guard.py`, { stdio: 'inherit' });
} catch {
  process.exit(1);
}

if (!data.timestamp || !data.nonce) {
  console.error("Missing anti-replay fields");
  process.exit(1);
}

const now = Date.now();
const age = Math.abs(now - data.timestamp);

if (age > 60000) {
  console.error("Replay attack detected (timestamp too old)");
  process.exit(1);
}

console.log("Signature verified (HMAC match).");
