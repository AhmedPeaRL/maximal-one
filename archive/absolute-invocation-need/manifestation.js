export function manifest() {
  return {
    timestamp: new Date().toISOString(),
    message: "Invocation occurred. Minimal presence acknowledged."
  };
}
