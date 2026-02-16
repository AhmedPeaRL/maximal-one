import { execSync } from "child_process";
import fs from "fs";
import crypto from "crypto";

function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

function stable(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort());
}

function main() {

  const commit = execSync("git rev-parse HEAD").toString().trim();

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

  const attestation = {
    commit,
    releaseHash: release.releaseHash,
    deterministicArtifactHash: release.artifactHash,
    scientificHash: release.scientificHash
  };

  const seal = sha256(stable(attestation));

  const final = {
    ...attestation,
    commitSeal: seal
  };

  fs.writeFileSync(
    "./core-scientific/commit-attestation/commit-seal.json",
    JSON.stringify(final, null, 2)
  );

  console.log("Commit Seal Generated:");
  console.log(seal);
}

main();
