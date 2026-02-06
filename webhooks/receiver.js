export async function receive(event) {
  const trace = {
    receivedAt: Date.now(),
    origin: event.headers?.["x-source"] ?? "unknown",
    body: event.body ?? null
  };

  // no response emitted
  return { received: true };
}
