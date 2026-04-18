import fs from "fs";

const SIGNAL_PATH = "./public/extracted_signal.json";
const OUTPUT_PATH = "./public/market_ready_signal.json";

function formatForMarket(signal) {
  return {
    title: "Irreducible Signal",
    timestamp: new Date().toISOString(),
    summary: signal.summary || "No summary",
    confidence: signal.confidence || 0,
    action: signal.action || "observe",
    raw: signal
  };
}

export function exportMarketSignal() {
  try {
    const raw = fs.readFileSync(SIGNAL_PATH, "utf-8");
    const signal = JSON.parse(raw);

    const formatted = formatForMarket(signal);

    fs.writeFileSync(
      OUTPUT_PATH,
      JSON.stringify(formatted, null, 2)
    );

    console.log("Market signal exported.");
  } catch (e) {
    console.error("Market export failed:", e.message);
  }
}
