import fs from "fs";
import path from "path";

export default function handler(req, res) {
  try {
    const filePath = path.join(process.cwd(), "data/latest_state.json");

    if (!fs.existsSync(filePath)) {
      return res.status(200).json({
        status: "no_state",
        message: "System has no state yet"
      });
    }

    const raw = fs.readFileSync(filePath, "utf-8");
    const data = JSON.parse(raw);

    return res.status(200).json({
      ok: true,
      state: data
    });

  } catch (e) {
    return res.status(500).json({
      ok: false,
      error: e.message
    });
  }
}
