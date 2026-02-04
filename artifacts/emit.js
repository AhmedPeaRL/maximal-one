const fs = require("fs");
const path = require("path");

function emit(artifact) {
  const filePath = path.join(__dirname, `${artifact.id}.json`);
  fs.writeFileSync(filePath, JSON.stringify(artifact, null, 2));
}

module.exports = { emit };
