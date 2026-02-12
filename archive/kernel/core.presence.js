/*
  MAXIMAL-ONE Core Presence
  This file executes nothing.
  It exists to be loaded.
*/

(function () {
  const CorePresence = {
    status: "present",
    executable: false,
    responds: false,
    timestamp: Date.now()
  };

  Object.freeze(CorePresence);

  if (typeof window !== "undefined") {
    window.MAXIMAL_ONE = CorePresence;
  }
})();
