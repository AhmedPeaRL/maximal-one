// silent-measurement.js
// Measurement without objectification

const SilentMeasurement = {
  traces: 0,

  registerTrace() {
    this.traces += 1;
    // No metadata.
    // No timestamp exposed.
    // No identity.
  },

  getState() {
    return {
      traces: this.traces,
      interpretation: null,
      action: null
    };
  }
};

export default SilentMeasurement;
