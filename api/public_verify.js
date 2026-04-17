export default async function handler(req, res) {
  try {
    const data = await fetch(
      "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/artifacts/global_verdict.json"
    );

    const json = await data.json();

    return res.json({
      ok: true,
      independent: true,
      verdict: json,
      source: "github-public"
    });

  } catch {
    return res.status(500).json({ ok: false });
  }
}
