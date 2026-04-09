export function normalizeRuntimeOutput(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort());
}
