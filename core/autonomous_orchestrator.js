import fs from "fs/promises";

export async function autonomousOrchestrator() {
  try {
    const validation = JSON.parse(
      await fs.readFile("./artifacts/anti_triviality_hard.json", "utf-8")
    );

    const signal = JSON.parse(
      await fs.readFile("./public/extracted_signal.json", "utf-8")
    );

    const pressure = await safeRead("./data/pressure_log.json");
    const prediction = await safeRead("./public/prediction_anchor.json");

    let decision = {
      action: "hold",
      reason: "insufficient coherence",
      confidence: 0
    };

    // -----------------------------
    // CORE LOGIC
    // -----------------------------

    const strongSignals = Object.values(validation).filter(
      v => v.hcm_better === true && v.confidence === "strong"
    );

    if (strongSignals.length >= 2) {
      decision = {
        action: "emit_artifact",
        reason: "multi-domain invariant confirmed",
        confidence: 0.85
      };
    }

    if (signal?.strength > 0.8 && pressure?.level < 0.4) {
      decision = {
        action: "open_market_gate",
        reason: "clean signal + low pressure",
        confidence: 0.9
      };
    }

    if (prediction?.irreversible === true) {
      decision = {
        action: "anchor_public_truth",
        reason: "irreversible structure detected",
        confidence: 0.95
      };
    }

    // -----------------------------
    // OUTPUT
    // -----------------------------

    await fs.writeFile(
      "./public/autonomous_decision.json",
      JSON.stringify(decision, null, 2)
    );

    return decision;

  } catch (e) {
    return {
      action: "error",
      reason: e.message
    };
  }
}

// helper
async function safeRead(path) {
  try {
    const data = await fs.readFile(path, "utf-8");
    return JSON.parse(data);
  } catch {
    return {};
  }
}
