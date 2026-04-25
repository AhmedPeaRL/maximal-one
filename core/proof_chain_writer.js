export async function appendProof(entry) {
  try {
    const res = await fetch('./public/proof_chain.json');
    const chain = await res.json();

    chain.entries.push(entry);

    await fetch('/api/update-proof-chain', {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(chain)
    });

  } catch (e) {
    console.log("Proof chain update failed");
  }
}
