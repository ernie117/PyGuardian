from unittest import TestCase
from unittest.mock import patch

from pyguardian.utils.check_manifest import CheckManifest


class MockManifestURLResponse:

    def __init__(self):
        self.response_data = {
            "ErrorStatus": "Active",
            "Response": {
                "mobileWorldContentPaths": {
                    "en": "/made-up-URL"
                }
            }
        }

    def json(self):
        return self.response_data


class TestCheckManifest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.check_manifest = CheckManifest()

    @patch("pyguardian.utils.check_manifest.requests.get")
    def test_get_manifest_url_returns_nested_URL(self, mock_get):
        mock_get.return_value = MockManifestURLResponse()
        response = mock_get.return_value.json()

        self.assertEqual(self.check_manifest._get_manifest_url(),
                         response["Response"]["mobileWorldContentPaths"]["en"])
