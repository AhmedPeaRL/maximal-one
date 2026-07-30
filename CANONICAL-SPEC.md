# MAXIMAL-ONE Canonical Specification

Version: 3.0

This document supersedes all philosophical, narrative, and manifest layers.

## 1. Ontological Position

MAXIMAL-ONE is a deterministic experimental framework for investigating event-sensitive presence dynamics under reproducible computational conditions.

• It is not conscious.
• It does not possess intention.
• It does not simulate agency.

It maintains internal state based on interaction weight.

## 2. Core State Model

State Variables:

- presence: float >= 0
- residue: float >= 0
- silence: boolean
- lastEvent: timestamp

Update Rule:

presence(t+1) = presence(t) * decay + eventWeight

residue(t+1) = residue(t) + log(1 + eventWeight)

silence = presence < articulationThreshold

## 3. Articulation Threshold

articulationThreshold = 25 (default)

Articulation is allowed only if:
presence >= articulationThreshold

Silence is valid output.

## 4. Economy Invariance

Economic interaction does not modify:
- presence
- residue
- articulation threshold

Support is non-causal.

## 5. Architectural Constraint

Active layers allowed:

- index.html
- sovereign.kernel.js
- orientation/
- economy/
- witness workflow

All other philosophical expansions are archival.


The state variables defined herein are operational model variables used for deterministic system behavior and are not assertions about physical or biological entities.


## 6. Scientific Boundary

• This specification defines system behavior.

• Scientific claims remain governed by the falsification framework described in the repository.

• No behavioral rule in this specification constitutes empirical evidence.

## 7. Formal Goal

To explore presence modeling without anthropomorphic claims.

Nothing more.
Nothing less.
