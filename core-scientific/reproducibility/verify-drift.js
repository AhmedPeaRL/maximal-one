import fs from "fs";
import crypto from "crypto";

function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

function stable(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort());
}

function main() {

  const releaseFiles = fs.readdirSync("./core-scientific/release-lock")
    .filter(f => f.startsWith("release-"))
    .sort()
    .reverse();

  if (releaseFiles.length === 0) {
    console.error("No release snapshot found.");
    process.exit(1);
  }

  const latest = releaseFiles[0];

  const release = JSON.parse(
    fs.readFileSync(`./core-scientific/release-lock/${latest}`)
  );

  const recomputedReleaseHash = sha256(stable({
    scientificHash: release.scientificHash,
    artifactHash: release.artifactHash,
    compositeSeal: release.compositeSeal
  }));

  if (recomputedReleaseHash !== release.releaseHash) {
    console.error("Drift detected in release snapshot.");
    process.exit(1);
  }

  console.log("Reproducibility Drift Guard: CLEAN");
}

main();
