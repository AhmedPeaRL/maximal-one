import fs from "fs";
import crypto from "crypto";

function sha256(x) {
  return crypto.createHash("sha256").update(x).digest("hex");
}

function main() {

  const pkg = JSON.parse(
    fs.readFileSync("./package.json", "utf8")
  );

  const version = pkg.version;

  const reportRaw = fs.readFileSync(
    "./core-scientific/publication-gate/report.json",
    "utf8"
  );

  const releaseHash = sha256(reportRaw);

  const releaseObject = {
    version,
    releaseHash
  };

  const releaseFileName =
    `release-${version}.json`;

  fs.writeFileSync(
    `./core-scientific/release-lock/${releaseFileName}`,
    JSON.stringify(releaseObject, null, 2) + "\n",
    "utf8"
  );

  console.log("Release frozen:", releaseFileName);
  console.log("Release Hash:", releaseHash);
}

main();
