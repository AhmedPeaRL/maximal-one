const fs = require('fs');

let data;

try {
  data = JSON.parse(fs.readFileSync('payload.json','utf8'));
} catch (e) {
  console.error("Malformed JSON");
  process.exit(1);
}

// Allow empty witness (controlled silence)
if (data._empty === true) {
  console.log("Empty witness allowed.");
  process.exit(0);
}

// === SEMANTIC VALIDATION ===

// must have at least one meaningful field
const meaningfulKeys = ["signal", "observation", "value", "claim"];

const hasMeaning = meaningfulKeys.some(k => k in data);

if (!hasMeaning) {
  console.error("No semantic meaning in payload");
  process.exit(1);
}

// reject null-heavy payloads
const values = Object.values(data);
const nullRatio = values.filter(v => v === null).length / values.length;

if (nullRatio > 0.5) {
  console.error("Payload too null-heavy");
  process.exit(1);
}

console.log("Semantic validation passed.");
