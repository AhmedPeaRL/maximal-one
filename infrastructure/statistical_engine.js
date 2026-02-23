// infrastructure/statistical_engine.js
// Strict Measurement & Spectral Analysis Engine

(function () {

  function mean(arr) {
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  }

  function variance(arr, m) {
    return arr.reduce((a, b) => a + Math.pow(b - m, 2), 0) / arr.length;
  }

  function std(arr, m) {
    return Math.sqrt(variance(arr, m));
  }

  function skewness(arr, m, s) {
    return mean(arr.map(x => Math.pow((x - m) / s, 3)));
  }

  function kurtosis(arr, m, s) {
    return mean(arr.map(x => Math.pow((x - m) / s, 4))) - 3;
  }

  function fft(signal) {
    const N = signal.length;
    const re = new Array(N).fill(0);
    const im = new Array(N).fill(0);

    for (let k = 0; k < N; k++) {
      for (let n = 0; n < N; n++) {
        const phi = (2 * Math.PI * k * n) / N;
        re[k] += signal[n] * Math.cos(phi);
        im[k] -= signal[n] * Math.sin(phi);
      }
    }

    return re.map((r, i) => Math.sqrt(r * r + im[i] * im[i]));
  }

  function analyze(data) {
    if (data.length < 32) return null;

    const m = mean(data);
    const s = std(data, m);
    const sk = skewness(data, m, s);
    const ku = kurtosis(data, m, s);
    const spectrum = fft(data);
    const dominant = spectrum.indexOf(Math.max(...spectrum.slice(1)));

    return {
      mean: m,
      std: s,
      skewness: sk,
      kurtosis: ku,
      dominantFrequencyIndex: dominant,
      sampleSize: data.length
    };
  }

  window.StatEngine = {
    analyze
  };
})();
