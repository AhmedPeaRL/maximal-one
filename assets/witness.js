/**
 * Witness Layer — Client Side
 * Role: Passive Observer
 * Function: Record presence, not request response
 */

(function () {
  const Witness = {
    init() {
      const form = document.getElementById("witness-form");
      const input = document.getElementById("witness-input");

      if (!form || !input) return;

      form.addEventListener("submit", function (event) {
        event.preventDefault();

        const content = input.value.trim();
        if (content.length === 0) return;

        Witness.observe(content);
        input.value = "";
      });
    },

    observe(content) {
      const payload = {
        content: content,
        timestamp: new Date().toISOString(),
        source: "maximal-one",
        classification: "presence-act",
        intent: "witness-only"
      };

      fetch("/witness/record.json", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }).catch(() => {
        // Silence is a valid outcome
      });
    }
  };

  document.addEventListener("DOMContentLoaded", Witness.init);
})();
       // silent submission
submitButton.addEventListener("click", () => {
  const content = witnessInput.value.trim();
  if (!content) return;

  // witness records, no promise
  fetch("/witness/record", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content })
  });

  witnessInput.value = "";
});

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("witness-input");
  const submit = document.getElementById("witness-submit");

  if (!input || !submit) return;

  submit.addEventListener("click", () => {
    const content = input.value.trim();
    if (!content) return;

    fetch("/witness/record", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content,
        at: new Date().toISOString(),
        origin: "maximal-one"
      })
    });

    input.value = "";
  });
});
