const fs = require('fs');
const crypto = require('crypto');

const payload = fs.readFileSync('payload.json', 'utf8');

const publicKey = process.env.WITNESS_PUBLIC_KEY;

if (!publicKey) {
  console.log("No public key — skipping signature verification");
  process.exit(0);
}

const signature = process.env.WITNESS_SIGNATURE;

if (!signature) {
  console.error("Missing signature");
  process.exit(1);
}

const verify = crypto.createVerify('SHA256');
verify.update(payload);
verify.end();

const isValid = verify.verify(publicKey, signature, 'base64');

if (!isValid) {
  console.error("Invalid signature");
  process.exit(1);
}

console.log("Signature verified.");
