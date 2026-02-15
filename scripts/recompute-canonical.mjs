import fs from "fs";
import crypto from "crypto";

const canonicalPath = new URL(
  "../core-scientific/publication-gate/canonical.json",
  import.meta.url
);

function stableStringify(obj) {
  if (obj === undefined) return "null";
  if (obj === null || typeof obj !== "object") {
    return JSON.stringify(obj);
  }

  if (Array.isArray(obj)) {
    return "[" + obj.map(stableStringify).join(",") + "]";
  }

  const keys = Object.keys(obj).sort();
  return (
    "{" +
    keys.map(k => JSON.stringify(k) + ":" + stableStringify(obj[k])).join(",") +
    "}"
  );
}

function computeHash(payload) {
  return crypto.createHash("sha256").update(payload).digest("hex");
}

const canonical = JSON.parse(fs.readFileSync(canonicalPath));

const canonicalHash = computeHash(
  stableStringify(canonical)
);

console.log("New canonicalHash:");
console.log(canonicalHash);
