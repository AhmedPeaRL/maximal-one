export const Rhythm = {
  state: "still",
  timestamp: Date.now(),
  observe() {
    this.timestamp = Date.now();
  }
};
