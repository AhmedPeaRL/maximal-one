const ALLOWED_ORIGIN = "https://ahmedpearl.github.io";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({
      ok: false,
      error: "method_not_allowed"
    });
  }

  if ((req.headers.origin || "") !== ALLOWED_ORIGIN) {
    return res.status(403).json({
      ok: false,
      error: "forbidden_origin"
    });
  }

  return res.status(410).json({
    ok: false,
    error: "market_execution_disabled",
    reason:
      "maximal-one scientific outputs do not authorize "
      + "financial execution."
  });
}
