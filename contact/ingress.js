export function receive(event) {
  return {
    received: true,
    responded: false,
    reason: "presence-only"
  };
}
