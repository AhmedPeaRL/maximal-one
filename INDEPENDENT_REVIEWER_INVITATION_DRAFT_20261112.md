# Independent Statistical Review Invitation — Draft

**Candidate reviewer:** Professor Anders Rahbek  
**Alternative candidate:** Professor Giuseppe Cavaliere  
**Status:** Draft for human approval and sending; no invitation has been sent.

## Why this candidate is suggested

Anders Rahbek co-authored a peer-reviewed paper with Giuseppe Cavaliere on bootstrap testing in time-series models, explicitly discussing test size and power. This is a relevant expertise match for the project's unresolved Type-I calibration and AR-surrogate design. Public publication information does not establish the candidate's availability, willingness, or absence of conflicts; those must be confirmed directly.

## Exact review materials to provide

- Repository: https://github.com/AhmedPeaRL/maximal-one
- Candidate source commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Current review-branch head: `8d38e605d84c3b8bc55393d88f87e9d40bd8fdc5`
- V4 candidate matrix: `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json`
- V4 matrix SHA-256: `f8b8dfaf97282ca24378b8929939d8fffd1fe72064a2fe662198422a11b1bc2f`
- V4 review request SHA-256: `616da863703ff157d3d95e2261308bf358e9ee16923695f6d6676db25937bb25`
- Exact snapshot run/artifact: `43072282939` / `13877613612`
- Snapshot manifest SHA-256: `9138d899529dd55b045f2507068850b57de4b4ee3027a3d91f64601efdc42fc0`
- Self-contained snapshot ZIP SHA-256: `a14c5a7347ff74dce5a34cad76d1cf362d6444e1a2a6bb2550695ac57d1fecfe`
- Inventory run/artifact: `43072014463` / `13877643344`
- Inventory SHA-256: `b30db3cb254f276a6d2707cbdbc4bef06f1dad92c4063c7098eedaae84154c92`

The candidate protocol is not frozen. The acceptance rule is unresolved. No formal calibration or confirmatory execution is authorized.

## Required reviewer response

Please state:

- whether you are willing and available to review;
- full name, current affiliation, and stable professional identity;
- relevant expertise in time-series inference, AR models, Monte Carlo calibration, and bootstrap/surrogate testing;
- prior involvement with the project (including none, if applicable);
- financial, professional, supervisory, collaborative, or other conflicts;
- exact commit and file hashes actually reviewed;
- a reasoned decision on estimand, Wilson sidedness, the proposed 0.075 ceiling, multiplicity, scenario coverage, invalid attempts, Monte Carlo precision, and implementation equivalence;
- disposition: `APPROVE_WITH_EXPLICIT_RATIONALE`, `REVISE_AND_RESUBMIT`, `REJECT`, or `INSUFFICIENT_INFORMATION`.

The reviewer is free to decline. No silence or non-response will be treated as approval.

## Draft email

Subject: Independent review request — Type-I calibration protocol for an AR-surrogate time-series test

Dear Professor Rahbek,

I am seeking an independent statistical-methods review of a computational time-series research project before any formal calibration or confirmatory execution is authorized.

The project uses a spectral endpoint and a fitted stationary Gaussian AR(p) surrogate procedure. The V4 candidate includes nine synthetic scenarios, including in-band resonant AR(2) cases. Its acceptance rule remains unresolved, and the protocol is explicitly not frozen.

I would be grateful if you would consider reviewing the exact candidate snapshot and advising whether the estimand, Type-I calibration design, acceptance rule, scenario coverage, Monte Carlo precision, invalid-attempt policy, and production-equivalence requirements are statistically defensible.

I will provide the exact source commit, matrix and request hashes, inventory, and self-contained review snapshot. The current project state does not claim a successful Type-I calibration, independent scientific replication, or support for the scientific hypothesis.

If you are unavailable, or if any conflict would prevent an independent review, I would appreciate a brief decline or referral to a suitably qualified reviewer.

Thank you for considering the request.

Sincerely,

Ahmed Salahuddin
Principal human researcher
AhmedPeaRL/maximal-one
