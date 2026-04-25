export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ ok: false });
  }

  try {
    const data = req.body;

    const gh = await fetch(
      "https://api.github.com/repos/ahmedpearl/maximal-one/contents/public/proof_chain.json",
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${process.env.GH_TOKEN}`,
          Accept: "application/vnd.github+json"
        },
        body: JSON.stringify({
          message: "update proof chain",
          content: Buffer.from(JSON.stringify(data, null, 2)).toString("base64")
        })
      }
    );

    if (!gh.ok) {
      return res.status(500).json({ ok: false });
    }

    return res.json({ ok: true });

  } catch (e) {
    return res.status(500).json({ ok: false });
  }
}
