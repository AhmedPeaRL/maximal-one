const witness = {
  observe(input) {
    const payload = {
      content: input,
      timestamp: new Date().toISOString(),
      source: "maximal-one",
      type: "presence-act"
    };

    fetch("/witness/record.json", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).catch(() => {
      // silence is acceptable
    });
  }
};
