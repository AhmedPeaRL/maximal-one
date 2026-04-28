import fs from "fs"
import crypto from "crypto"

const HISTORY_PATH = ".coherence-memory/history.log"

function loadHistory() {
  if (!fs.existsSync(HISTORY_PATH)) return []
  return fs.readFileSync(HISTORY_PATH, "utf8")
    .split("\n")
    .filter(Boolean)
}

function computeFieldStability(history) {
  const frequency = {}

  history.forEach(h => {
    frequency[h] = (frequency[h] || 0) + 1
  })

  const max = Math.max(...Object.values(frequency), 1)
  const dominant = Object.entries(frequency)
    .sort((a, b) => b[1] - a[1])[0]

  return {
    dominant_hash: dominant ? dominant[0] : null,
    stability_score: dominant ? dominant[1] / history.length : 1,
    total_runs: history.length
  }
}

function main() {
  const history = loadHistory()
  const score = computeFieldStability(history)

  fs.writeFileSync(
    "core-scientific/stability/attractor-score.json",
    JSON.stringify(score, null, 2)
  )

  console.log("Attractor field score generated.")
}

main()
