const retiredResponse = () =>
  new Response(
    JSON.stringify({ ok: false, retired: true }),
    {
      status: 410,
      headers: {
        "content-type": "application/json",
        "cache-control": "no-store"
      }
    }
  );

export async function onRequest() {
  return retiredResponse();
}

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");

  return res.status(410).json({
    ok: false,
    retired: true
  });
}
