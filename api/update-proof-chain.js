const ALLOWED_ORIGIN = "https://ahmedpearl.github.io";

function validOrigin(req) {
  const origin = req.headers.origin || "";

  return origin === ALLOWED_ORIGIN;
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({
      ok: false,
      error: "method_not_allowed"
    });
  }

  if (!validOrigin(req)) {
    return res.status(403).json({
      ok: false,
      error: "forbidden_origin"
    });
  }

  return res.status(410).json({
    ok: false,
    error: "proof_chain_mutation_disabled",
    reason:
      "Public proof-chain mutation is disabled. "
      + "Scientific artifacts are produced only by "
      + "the controlled validation pipeline."
  });
}
