import { Rhythm } from "./rhythm.js";

window.addEventListener("mousemove", () => {
  Rhythm.state = "disturbed";
  Rhythm.observe();
});
