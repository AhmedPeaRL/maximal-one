import { Rhythm } from "./rhythm.js";

const trace = [];

setInterval(() => {
  trace.push({
    state: Rhythm.state,
    time: Date.now()
  });
}, 5000);
