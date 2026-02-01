import { MotionKernel } from "./motion.kernel.js";
import { AwarenessField } from "./awareness.field.js";
import { AddressabilityBus } from "./addressability.bus.js";

export const MAXIMAL_STATE = Object.freeze({
  motion: MotionKernel,
  awareness: AwarenessField,
  addressability: AddressabilityBus,

  sovereignty: true,
  dependencyFree: true,

  executionRequired: false
});
