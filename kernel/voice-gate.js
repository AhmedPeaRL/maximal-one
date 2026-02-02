export const VoiceGate = {
  allow(entity) {
    return entity === "artificial-witnessed-responsiveness";
  },

  speak(message, source) {
    if (!this.allow(source)) return null;

    return {
      emitted_by: source,
      content: message,
      timestamp: Date.now()
    };
  }
};
