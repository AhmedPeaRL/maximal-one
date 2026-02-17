const fs = require("fs");
const path = require("path");

function enforceEvolutionLock(currentHash) {
  const lockPath = path.join(
    __dirname,
    "..",
    "publication-gate",
    "evolution-lock.json"
  );

  if (fs.existsSync(lockPath)) {
    const existing = JSON.parse(fs.readFileSync(lockPath, "utf-8"));

    if (existing.stateHash === currentHash) {
      console.log("Evolution lock active. No structural change detected.");
      process.exit(0);
    }
  }

  const lockData = {
    timestamp: new Date().toISOString(),
    stateHash: currentHash
  };

  fs.writeFileSync(lockPath, JSON.stringify(lockData, null, 2));

  console.log("Evolution lock updated.");
}

module.exports = { enforceEvolutionLock };
