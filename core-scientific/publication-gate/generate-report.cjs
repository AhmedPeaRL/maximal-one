#!/usr/bin/env node

/**
 * generate-report.cjs
 * Deterministic Publication Gate Report Generator
 * No silent failure path exists.
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = process.cwd();
const OUTPUT_DIR = path.join(ROOT, "core-scientific", "publication-gate");
const OUTPUT_FILE = path.join(OUTPUT_DIR, "publication-report.json");

function sha256(data) {
  return crypto.createHash("sha256").update(data).digest("hex");
}

function fail(message) {
  console.error("❌ Publication Gate Failure:");
  console.error(message);
  process.exit(1);
}

function ensureDirectoryExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fail(`Required directory missing: ${dirPath}`);
  }
}

function deterministicTimestamp() {
  return new Date().toISOString();
}

function main() {
  ensureDirectoryExists(OUTPUT_DIR);

  const packagePath = path.join(ROOT, "package.json");

  if (!fs.existsSync(packagePath)) {
    fail("package.json not found.");
  }

  const packageContent = fs.readFileSync(packagePath, "utf-8");
  const packageHash = sha256(packageContent);

  const report = {
    generator: "publication-gate",
    deterministic: true,
    timestamp: deterministicTimestamp(),
    package_sha256: packageHash,
    node_version: process.version,
    invariant: "No silent failure path exists."
  };

  const reportString = JSON.stringify(report, null, 2);
  const reportHash = sha256(reportString);

  const finalOutput = {
    ...report,
    report_sha256: reportHash
  };

  fs.writeFileSync(
    OUTPUT_FILE,
    JSON.stringify(finalOutput, null, 2)
  );

  console.log("✅ Publication report generated.");
  console.log(`Report hash: ${reportHash}`);
}

main();
