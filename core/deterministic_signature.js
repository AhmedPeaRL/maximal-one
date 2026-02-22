// deterministic_signature.js
// Generates structural hash of full DOM

(function () {

  async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  async function generateSignature() {
    const domContent = document.documentElement.outerHTML;
    const signature = await sha256(domContent);

    const payload = {
      timestamp: new Date().toISOString(),
      domLength: domContent.length,
      signature: signature
    };

    console.log("MAXIMAL_SIGNATURE:", JSON.stringify(payload));
    return payload;
  }

  window.addEventListener("load", function () {
    generateSignature();
  });

})();
