export async function externalWitnessAnchor(payload) {
  const encoder = new TextEncoder();
  const data = encoder.encode(JSON.stringify(payload));

  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");

  // bind to public external timestamp (uncontrollable)
  const res = await fetch("https://worldtimeapi.org/api/timezone/Etc/UTC");
  const timeData = await res.json();

  return {
    hash: hashHex,
    external_time: timeData.utc_datetime,
    source: "worldtimeapi.org"
  };
}
