import crypto from "crypto";

export async function onRequestGet() {
  try {
    const res = await fetch(
      "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/public/live_truth.json"
    );

    const truth = await res.json();

    return new Response(JSON.stringify({
      integrity: truth.integrity?.report_hash ? "bound" : "unverified",
      decision: truth.decision?.global,
      confidence: truth.scientific_signal?.confidence
    }), {
      headers: { "Content-Type": "application/json" }
    });

  } catch (e) {
    return new Response(JSON.stringify({
      integrity: "error",
      decision: "unknown",
      confidence: 0
    }));
  }
}

export default async function handler(req, res) {
  try {
    const truthRes = await fetch(
      "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/public/live_truth.json"
    );

    const reportRes = await fetch(
      "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/artifacts/canonical_report.json"
    );

    const hashRes = await fetch(
      "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/artifacts/report.hash"
    );

    const truth = await truthRes.json();
    const reportText = await reportRes.text();
    const storedHash = (await hashRes.text()).trim();

    const calculatedHash = crypto
      .createHash("sha256")
      .update(reportText)
      .digest("hex");

    const integrity = calculatedHash === storedHash;

    return res.json({
      ok: true,
      integrity,
      calculated_hash: calculatedHash,
      stored_hash: storedHash,
      decision: truth?.decision?.global || "unknown",
      confidence: truth?.scientific_signal?.confidence || null
    });

  } catch (e) {
    return res.status(500).json({
      ok: false,
      error: "verification_failed"
    });
  }
}
