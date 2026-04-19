export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ ok: false });
  }

  const body = req.body;

  console.log("THNDR DISPATCH:", body);

  // هنا تقدر تبعت Notification أو Telegram أو Email

  return res.status(200).json({
    ok: true,
    received: body
  });
}
