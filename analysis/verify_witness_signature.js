import crypto from "crypto";
import fs from "fs";

const SECRET = process.env.WITNESS_SECRET || "fallback_secret";

function generateSignature(payload) {
  return crypto
    .createHmac("sha256", SECRET)
    .update(JSON.stringify(payload))
    .digest("hex");
}

function verify(payload, signature) {
  const expected = generateSignature(payload);
  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(signature)
  );
}

const raw = fs.readFileSync("payload.json", "utf8");
const data = JSON.parse(raw);

if (data._empty === true) {
  console.log("Empty payload allowed.");
  process.exit(0);
}

const { signature, ...rest } = data;

if (!signature) {
  console.error("Missing signature.");
  process.exit(1);
}

if (!verify(rest, signature)) {
  console.error("Invalid signature.");
  process.exit(1);
}

console.log("Signature verified.");
