// non-invocative-support.js
// Support may occur, but is never invoked.

const EffectBoundary = {effect-permits-support/engine/non-invocative-support.js
  observe(effect) {
    // The system observes effect only
    return effect && effect.exists === true;
  },

  permitSupport() {
    // Permission is passive, not an action
    return true;
  },

  receiveSupport() {
    // Intentionally empty
    // No receipt
    // No acknowledgment
    // No adaptation
  }
};

export default EffectBoundary;
