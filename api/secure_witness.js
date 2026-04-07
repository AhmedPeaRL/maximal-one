export async function sendWitnessSecure(payload) {
  const response = await fetch("/.netlify/functions/witness", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error("Failed to send witness");
  }

  return true;
}
