const { computeSelfMetric } = require('./self-metric.cjs');
const { enforceInvariants } = require('./invariant-enforcer.cjs');
const { executeTransition } = require('../state-engine/state-machine.cjs');
const { enforceEvolutionLock } = require("./evolution-lock.cjs");

function generateAutonomousEvent() {
  enforceInvariants();

  const metric = computeSelfMetric();

  const event = {
    type: "ARCHITECTURAL_EXTENSION",
    metricHash: metric.metricHash,
    numericScore: metric.numericScore,
    timestamp: new Date().toISOString()
  };

  const newStateHash = executeTransition(event);

  console.log("Autonomous transition executed.");
  console.log("New state hash:", newStateHash);

  return newStateHash;
}

const transition = executeTransition();
enforceEvolutionLock(transition.stateHash);

generateAutonomousEvent();
