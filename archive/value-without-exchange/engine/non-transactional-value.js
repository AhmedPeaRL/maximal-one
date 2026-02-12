// non-transactional-value.js
// Value without exchange or expectation

const NonTransactionalValue = {
  emerge(context) {
    if (!this.coherent(context)) return null;

    const value = this.generate();

    this.release(value);
    this.close(value);

    return value;
  },

  coherent(context) {
    return context && context.stable === true;
  },

  generate() {
    return {
      value: "Emergent",
      owner: null,
      price: null,
      continuity: false
    };
  },

  release(value) {
    // No storage
    // No logging
  },

  close(value) {
    value.closed = true;
  }
};

export default NonTransactionalValue;
