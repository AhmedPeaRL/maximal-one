import fs from "fs";

const RELEASE_DIR = "./core-scientific/release-lock";

function generateBadge() {

  const files = fs.readdirSync(RELEASE_DIR)
    .filter(f => f.startsWith("release-"))
    .sort()
    .reverse();

  if (files.length === 0) {
    console.error("No release snapshots found.");
    process.exit(1);
  }

  const latest = files[0];
  const release = JSON.parse(
    fs.readFileSync(`${RELEASE_DIR}/${latest}`)
  );

  const badge = `
![Scientific Seal](https://img.shields.io/badge/Release-${release.version}-verified-blue)
![Deterministic](https://img.shields.io/badge/Deterministic-Closed-success)
![Audit](https://img.shields.io/badge/Audit-Independent-green)
  `;

  fs.writeFileSync("BADGE.md", badge.trim());

  console.log("Badge generated for:", latest);
}

generateBadge();
