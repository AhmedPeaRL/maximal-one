const fs = require('fs');
const crypto = require('crypto');

const payload = fs.readFileSync('payload.json', 'utf8');

const expectedSignature = process.env.WITNESS_SIGNATURE;

if (!expectedSignature) {
  console.log("No signature — skipping verification");
  process.exit(0);
}

const actualSignature = crypto
  .createHash('sha256')
  .update(payload)
  .digest('hex');

if (actualSignature !== expectedSignature) {
  console.error("Invalid signature (hash mismatch)");
  process.exit(1);
}

console.log("Signature verified (hash match).");
