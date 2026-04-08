import fs from "fs";
import path from "path";

const policy = JSON.parse(
  fs.readFileSync("policy/hcm_alignment.json", "utf8")
);

function scanFile(filePath) {
  const content = fs.readFileSync(filePath, "utf8");

  for (const forbidden of policy.forbidden_patterns) {
    if (content.includes(forbidden)) {
      throw new Error(`Forbidden pattern "${forbidden}" in ${filePath}`);
    }
  }
}

function scanDir(dir) {
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const full = path.join(dir, file);

    if (fs.statSync(full).isDirectory()) {
      scanDir(full);
    } else if (file.endsWith(".js")) {
      scanFile(full);
    }
  }
}

try {
  scanDir("core");
  console.log("Alignment OK");
} catch (e) {
  console.error(e.message);
  process.exit(1);
    }
