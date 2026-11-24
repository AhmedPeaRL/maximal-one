"""Regression tests for retired legacy external-reproduction helpers."""

import contextlib
import io
import unittest
from unittest.mock import patch

from api.public_reproduce_endpoint import run_external_reproduction
from analysis import external_reproduction


class RetiredExternalReproductionTests(unittest.TestCase):
    def test_public_helper_fails_closed_without_side_effects(self):
        with patch("subprocess.run") as run:
            with self.assertRaisesRegex(RuntimeError, "PUBLIC_REPRODUCTION_HELPER_RETIRED"):
                run_external_reproduction({"arbitrary": "payload"})
            run.assert_not_called()

    def test_legacy_fetcher_never_claims_reproduction(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = external_reproduction.main()
        self.assertEqual(code, 2)
        self.assertIn("DISABLED_NOT_A_REPRODUCTION", output.getvalue())
        self.assertIn('"independent_implementation_replication": false', output.getvalue())
        self.assertIn('"scientific_claim_authority": false', output.getvalue())


if __name__ == "__main__":
    unittest.main()
