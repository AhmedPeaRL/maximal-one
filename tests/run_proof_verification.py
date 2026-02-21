import sys
import os

# Allow test folder to access root directory
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from proof_harness import LinearSystem, TheoreticalVerifier


def run_verification():
    system = LinearSystem(
        A=[[0.8]],
        B=[[0.1]],
        M=0.5
    )

    verifier = TheoreticalVerifier(system)
    result = verifier.verify()

    assert result["stable"], "System is not theoretically stable."

    print("Verification successful.")
    print("Spectral radius squared:", result["spectral_radius_squared"])
    print("Ultimate bound:", result["ultimate_bound"])


if __name__ == "__main__":
    run_verification()
