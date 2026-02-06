export default function handler(req, res) {
  const { input } = req.body;

  if (!input || input.trim().length < 20) {
    res.status(204).end();
    return;
  }

  if (input.includes("prove") || input.includes("truth")) {
    res.status(200).send("Minimal response permitted.");
    return;
  }

  res.status(204).end();
}
