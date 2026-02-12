import { Rhythm } from "./rhythm.js";

setInterval(() => {
  if (Date.now() - Rhythm.timestamp > 3000) {
    Rhythm.state = "still";
  }
}, 1000);
