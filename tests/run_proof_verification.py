import sys
import os

# Ensure project root is in Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from proof_harness import DynamicalSystem, LyapunovVerifier


def run_verification():
    system = DynamicalSystem()
    verifier = TheoreticalVerifier(system)

    result = verifier.verify()
    assert result["stable"], "System is not theoretically stable."

    if not result["stable"]:
        raise AssertionError("System failed Lyapunov stability check.")

    print("Proof verification passed.")
    return True


if __name__ == "__main__":
    run_verification()
