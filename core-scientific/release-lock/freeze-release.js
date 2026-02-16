import fs from "fs";
import crypto from "crypto";

const REPORT_PATH = "./core-scientific/publication-gate/report.json";
const RELEASE_DIR = "./core-scientific/release-lock";

function stableStringify(obj) {
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

function assert(condition, message) {
  if (!condition) {
    console.error("RELEASE FREEZE FAILED:", message);
    process.exit(1);
  }
}

function freezeRelease() {

  assert(fs.existsSync(REPORT_PATH), "Report missing");

  const report = JSON.parse(fs.readFileSync(REPORT_PATH));

  const version = report.protocolVersion;
  const artifactHash = report.deterministicArtifactHash;

  const releaseObject = {
    version,
    artifactHash,
    scientificHash: report.scientificHash,
    compositeSeal: report.compositeSeal,
    canonicalHash: report.canonicalHash,
    frozenAt: new Date().toISOString()
  };

  const releaseHash = computeHash(stableStringify(releaseObject));

  const finalRelease = {
    ...releaseObject,
    releaseHash
  };

  if (!fs.existsSync(RELEASE_DIR)) {
    fs.mkdirSync(RELEASE_DIR, { recursive: true });
  }

  const fileName = `release-${version}.json`;

  fs.writeFileSync(
    `${RELEASE_DIR}/${fileName}`,
    JSON.stringify(finalRelease, null, 2)
  );

  console.log("Release frozen:", fileName);
  console.log("Release Hash:", releaseHash);
}

freezeRelease();
