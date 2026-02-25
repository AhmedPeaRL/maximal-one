const fs = require("fs");
const crypto = require("crypto");

const data = JSON.parse(
  fs.readFileSync("artifacts/canonical_report.json","utf8")
);

const serialized = JSON.stringify(data.report);
const recalculated = crypto
  .createHash("sha256")
  .update(serialized)
  .digest("hex");

if (recalculated !== data.sha256) {
  console.log(JSON.stringify({passed:false,reason:"hash_mismatch"}));
  process.exit(1);
}

const variance = data.report.stability.variance;

const threshold = 0.05;

if (variance > threshold) {
  console.log(JSON.stringify({passed:false,reason:"unstable_variance"}));
  process.exit(1);
}

console.log(JSON.stringify({passed:true}));
