export async function ingest(request) {
  const event = {
    timestamp: Date.now(),
    source: "api",
    payload: request.body ?? null
  };

  return {
    accepted: true,
    contained: true,
    expressed: false
  };
}
