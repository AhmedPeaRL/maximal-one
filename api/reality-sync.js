import fs from "fs";
import path from "path";

export default async function handler(req, res) {
  try {
    const response = await fetch(
      "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/public/live_truth.json"
    );

    const data = await response.json();

    return res.json({
      ok: true,
      state: data
    });

  } catch (e) {
    return res.status(500).json({
      ok: false,
      error: "sync_failed"
    });
  }
}
