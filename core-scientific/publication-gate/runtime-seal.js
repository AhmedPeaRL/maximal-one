import crypto from "crypto";
import os from "os";

function stableStringify(obj) {
  if (obj === undefined) return "null";
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

export function computeRuntimeSeal() {

  const runtimeFingerprint = {
    nodeVersion: process.version,
    platform: process.platform,
    arch: process.arch,
    cpuModel: os.cpus()?.[0]?.model || "unknown",
    cpuCount: os.cpus()?.length || 0,
    totalMemory: os.totalmem(),
    hostname: os.hostname()
  };

  const runtimeHash = computeHash(
    stableStringify(runtimeFingerprint)
  );

  const environmentClass =
    process.env.GITHUB_ACTIONS === "true"
      ? "github-runner"
      : "local-node";

  return {
    runtimeHash,
    fingerprint: runtimeFingerprint,
    environmentClass
  };
}
