import fs from "fs";
import path from "path";

// ✅ deterministic JSON load (no import assertions)
const intent = JSON.parse(
  fs.readFileSync(new URL("../core/intent_signature.json", import.meta.url))
);

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

function checkIntentAlignment(output) {
  if (!output) return false;

  const str = JSON.stringify(output).toLowerCase();

  for (const forbidden of intent.forbidden_patterns) {
    if (str.includes(forbidden)) {
      throw new Error("Intent violation: " + forbidden);
    }
  }

  return true;
}
