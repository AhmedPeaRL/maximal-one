const fs = require("fs");
const path = require("path");

function coldStore(payload) {
  const dir = path.join(__dirname, "artifacts");
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  const file = path.join(dir, `artifact-${Date.now()}.json`);
  fs.writeFileSync(file, JSON.stringify(payload, null, 2));
}

module.exports = { coldStore };
