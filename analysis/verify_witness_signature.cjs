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

const expected = crypto
  .createHmac('sha256', secret)
  .update(JSON.stringify(payloadWithoutSig))
  .digest('hex');

if (signature !== expected) {
  console.error("Invalid signature (HMAC mismatch)");
  process.exit(1);
}

console.log("Signature verified (HMAC match).");
