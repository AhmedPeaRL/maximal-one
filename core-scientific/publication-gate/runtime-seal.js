import crypto from "crypto";
import os from "os";
import process from "process";

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

export function computeRuntimeSeal() {

  const fingerprint = {
    nodeVersion: process.version,
    platform: process.platform,
    arch: process.arch,
    openssl: process.versions.openssl,
    v8: process.versions.v8,
    cpuModel: os.cpus()[0]?.model || "unknown"
  };

  const hash = crypto
    .createHash("sha256")
    .update(stableStringify(fingerprint))
    .digest("hex");

  return {
    fingerprint,
    runtimeHash: hash
  };
}
