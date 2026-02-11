(function () {
  const continuity = {
    exists: true,
    requiresSupport: false,
    reactsToSupport: false,
    changesWithTime: false,
    state() {
      return "continuous";
    }
  };

  // Silent assertion
  Object.freeze(continuity);

  // No export. No invocation.
})();
