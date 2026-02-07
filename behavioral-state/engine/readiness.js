// readiness.js
// Active Behavioral Readiness Engine
// This engine does not trigger responses.
// It only maintains readiness.

const ReadinessState = {
  active: true,
  pressured: false,
  lastInvocation: null,

  receiveInvocation(signal) {
    this.pressured = true;
    this.lastInvocation = {
      signal,
      timestamp: Date.now()
    };
    // No response is triggered here.
  },

  resetPressure() {
    this.pressured = false;
    this.lastInvocation = null;
  }
};

export default ReadinessState;
