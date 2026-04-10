import fs from "fs";
import path from "path";

export default async function handler(req, res) {
  try {
    const artifactPath = path.join(process.cwd(), "data");

    if (!fs.existsSync(artifactPath)) {
      return res.json({
        ok: false,
        reason: "no-artifacts"
      });
    }

    const files = fs.readdirSync(artifactPath)
      .filter(f => f.endsWith(".json"))
      .sort((a, b) => b.localeCompare(a));

    if (files.length === 0) {
      return res.json({
        ok: false,
        reason: "empty"
      });
    }

    const latest = files[0];

    const content = JSON.parse(
      fs.readFileSync(path.join(artifactPath, latest), "utf8")
    );

    res.json({
      ok: true,
      timestamp: latest,
      state: content
    });

  } catch (e) {
    res.json({
      ok: false,
      error: e.message
    });
  }
}
