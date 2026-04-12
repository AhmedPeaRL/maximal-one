const fs = require('fs');
const crypto = require('crypto');

const payload = fs.readFileSync('payload.json', 'utf8');

const secret = process.env.WITNESS_SECRET;

if (!secret) {
  console.log("No secret — skipping verification");
  process.exit(0);
}

const expected = crypto
  .createHmac('sha256', secret)
  .update(payload)
  .digest('hex');

const incoming = JSON.parse(payload).signature;

if (!incoming) {
  console.error("Missing signature");
  process.exit(1);
}

if (incoming !== expected) {
  console.error("Invalid signature (HMAC mismatch)");
  process.exit(1);
}

console.log("Signature verified (HMAC match).");
