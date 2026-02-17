const fs = require("fs");
const path = require("path");

function enforceEvolutionLock(stateHash) {
  const lockPath = path.join(__dirname, "evolution-lock.json");

  if (fs.existsSync(lockPath)) {
    const previous = JSON.parse(fs.readFileSync(lockPath, "utf-8"));

    if (previous.stateHash === stateHash) {
      console.log("Evolution lock active. No state change.");
      process.exit(0);
    }
  }

  fs.writeFileSync(
    lockPath,
    JSON.stringify(
      {
        timestamp: new Date().toISOString(),
        stateHash
      },
      null,
      2
    )
  );

  console.log("Evolution lock updated.");
}

module.exports = { enforceEvolutionLock };
