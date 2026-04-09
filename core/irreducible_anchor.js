import crypto from "crypto";

/**
 * Irreducible Reality Anchor
 * Binds system state to non-controllable external signals
 */

export async function bindIrreducibleReality() {
  const anchors = [];

  // 1) Time Anchor (Non-reversible)
  const now = Date.now();
  anchors.push({
    type: "time",
    value: now,
  });

  // 2) Public entropy (cannot be faked easily)
  try {
    const res = await fetch("https://worldtimeapi.org/api/ip", { cache: "no-store" });
    const data = await res.json();

    anchors.push({
      type: "world_time_api",
      value: data.utc_datetime || null,
    });
  } catch {
    anchors.push({
      type: "world_time_api",
      value: "unreachable",
    });
  }

  // 3) Browser entropy
  anchors.push({
    type: "navigator",
    value: navigator.userAgent,
  });

  // 4) Screen entropy
  anchors.push({
    type: "screen",
    value: `${window.innerWidth}x${window.innerHeight}`,
  });

  // 5) Hash everything
  const raw = JSON.stringify(anchors);

  const hash = crypto
    .createHash("sha256")
    .update(raw)
    .digest("hex");

  return {
    anchors,
    hash,
    timestamp: now,
  };
}
