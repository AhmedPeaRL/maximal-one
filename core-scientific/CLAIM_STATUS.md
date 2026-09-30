Claim Status

Current Status

UNDER INVESTIGATION

The current canonical pipeline does not support promotion of the
Constrained Spectral Persistence Hypothesis.

The machine-gated scientific claim remains closed because the declared
primary stochastic null has not been rejected.

Canonical Primary Result

Primary dataset:

"real-data/sunspots_full.csv"

Canonical sample size:

"N = 3328"

Canonical Welch spectral exponent:

"alpha = 2.525347"

Independent FFT-periodogram estimate:

"alpha = 2.423397"

Welch/FFT agreement:

"delta = 0.101950"

The cross-method agreement is within the declared numerical validation
threshold.

Primary Stochastic Null

The declared primary stochastic null is:

"stationary_gaussian_AR_p_aic"

with:

- AIC order selection from 1 through 20
- stationary Gaussian AR(p) surrogate generation
- refitting of the selected order for each surrogate
- canonical primary alpha as the endpoint
- upper-tail "greater_than_null" testing
- 1000 valid surrogate trials
- add-one Monte Carlo p-value

Current result:

"observed alpha = 2.525347"

"null mean = 3.197386"

"null q05 = 2.816685"

"null q95 = 3.584700"

"exceedances = 999 / 1000"

"p = 0.999001"

"reject_at_0_05 = false"

Therefore the primary stochastic null is not rejected.

Scientific claim promotion is correctly blocked.

Null Calibration Warning

The current surrogate ensemble reports:

"surrogate_boundary_fraction = 0.965"

and the selected observed order reaches:

"order = 20"

the declared maximum.

This does not constitute evidence for or against the scientific hypothesis.

It indicates that the declared finite AR order range requires additional
model-capacity calibration before stronger inferential conclusions are
drawn from this null family.

The calibration warning must not be resolved by changing the protocol solely
to obtain claim support.

Secondary Statistical Diagnostics

The permutation null reports:

"p = 0.0002"

This result is explicitly diagnostic-only.

It is evidence against the specified exchangeability/permutation null only.
It is not the authoritative primary stochastic-null result and cannot
override the primary AR-null result.

The separation diagnostic reports:

"z = 11.743516"

This is also diagnostic-only and is not independent evidence for the
scientific claim.

Multi-Scale Diagnostic

The current canonical multi-scale diagnostic reports:

"pairwise delta = 0.482583"

"relative dispersion = 0.205825"

The declared diagnostic criterion is satisfied in the current run.

This does not establish the scientific claim.

Independent Real-Domain Replication

Two independent real domains currently have valid alpha measurements:

- CO2 atmospheric data
- Cosmic-ray data

Their valid measurements do not by themselves establish replication.

The authoritative replication gate requires each domain to reject the same
declared primary stochastic null using the same endpoint, direction, tail,
and null family.

Current result:

"Passed = 0 / 2"

Therefore independent scientific replication is NOT ESTABLISHED.

Derived datasets, shuffled datasets, synthetic datasets, and null controls
do not count as independent replication.

Computational Reproducibility

The clean-checkout computational reproduction currently verifies:

- exact checkout
- canonical report structure match
- fingerprint match
- canonical alpha agreement

This establishes computational reproducibility of the declared pipeline.

It does not establish:

- independent scientific replication
- independent implementation replication
- laboratory replication
- causality
- mechanism
- universality

Prediction

The current train/test diagnostic does not establish predictive validity.

Current structural match:

"false"

Therefore it must remain diagnostic.

Epistemic Boundary

The current evidence does not establish:

- HCM causation
- consciousness
- NeuroEnergetic Field existence
- a universal law
- novel physics
- mechanism
- universal cross-domain behavior
- market advantage
- trading validity

These remain hypotheses requiring independent empirical tests.

Required Next Scientific Steps

1. Complete a justified calibration of the primary stochastic-null family.
2. Declare the confirmatory null protocol before a fresh validation run.
3. Declare independent replication domains before evaluating their results.
4. Require domain-level rejection of the same primary null for replication.
5. Preserve the current negative primary result rather than tuning the protocol
   around it.
6. Obtain independent reproduction outside the original execution environment.
7. Preserve all negative and positive controls as first-class artifacts.

No threshold should be changed solely to convert the current state into PASS.
No diagnostic statistic may be promoted into primary evidence.

Current scientific status: UNDER INVESTIGATION.
