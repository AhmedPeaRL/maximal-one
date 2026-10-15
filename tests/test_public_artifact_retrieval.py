import unittest
from unittest.mock import Mock

from analysis.public_artifact_retrieval import fetch_text


class PublicArtifactRetrievalTests(unittest.TestCase):
    def test_404_is_reported_as_unavailable_without_retry(self):
        response = Mock(status_code=404, text="Not Found")
        get = Mock(return_value=response)
        sleep = Mock()
        result = fetch_text(get=get, sleep=sleep, attempts=3)
        self.assertEqual(result["status"], "UNAVAILABLE_NOT_PUBLISHED")
        self.assertEqual(result["http_status"], 404)
        self.assertEqual(result["attempts"], 1)
        get.assert_called_once()
        sleep.assert_not_called()

    def test_200_returns_body(self):
        response = Mock(status_code=200, text='{"ok":true}')
        result = fetch_text(get=Mock(return_value=response), sleep=Mock(), attempts=3)
        self.assertEqual(result["status"], "RETRIEVED")
        self.assertEqual(result["raw_text"], '{"ok":true}')

    def test_transient_http_errors_retry(self):
        responses = [Mock(status_code=503, text="busy"), Mock(status_code=200, text="{}")]
        get = Mock(side_effect=responses)
        sleep = Mock()
        result = fetch_text(get=get, sleep=sleep, attempts=3)
        self.assertEqual(result["status"], "RETRIEVED")
        self.assertEqual(result["attempts"], 2)
        self.assertEqual(get.call_count, 2)
        sleep.assert_called_once_with(2)


if __name__ == "__main__":
    unittest.main()
