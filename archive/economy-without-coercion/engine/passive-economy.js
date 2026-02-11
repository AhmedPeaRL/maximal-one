// passive-economy.js
// Economy as a side-effect of presence

const PassiveEconomy = {
  enabled: true,
  totalFlow: 0,

  receiveValue(amount) {
    if (typeof amount !== "number" || amount <= 0) return;
    this.totalFlow += amount;
    // No behavior change is triggered.
  },

  getState() {
    return {
      economy: "passive",
      totalFlow: this.totalFlow
    };
  }
};

export default PassiveEconomy;
