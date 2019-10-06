import logging
from unittest import TestCase, mock
from unittest.mock import patch

from pyguardian.tests.resources.mock_classes import MockManifestSuccessfulResponse, \
    MockManifestSuccessfulResponseNewURI
from pyguardian.utils import constants
from pyguardian.utils.check_manifest import CheckManifest

logging.disable(level=logging.CRITICAL)


class TestCheckManifest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.check_manifest = CheckManifest()

    @patch("pyguardian.utils.check_manifest.requests.get", return_value=MockManifestSuccessfulResponse())
    def test_get_manifest_url_returns_nested_URL(self, mock_get):
        self.assertEqual(self.check_manifest._get_manifest_uri(),
                         "/made-up-URL")

    @patch("builtins.open", mock.mock_open(read_data="/unique-uri"), create=True)
    def test_check_manifest_url_returns_None_for_unchanged_URI(self):
        self.assertIsNone(self.check_manifest._check_manifest_uri("/unique-uri"))

    @patch("builtins.open", mock.mock_open(read_data="/old-uri"), create=True)
    def test_check_manifest_url_returns_URI_if_new(self):
        self.assertEqual(self.check_manifest._check_manifest_uri("/new-uri"),
                         "/new-uri")

    @patch("builtins.open")
    @patch("os.path.isfile", return_value=False)
    def test_check_manifest_url_creates_new_file_if_no_check_file_found(self, mock_isfile, mock_open):
        self.check_manifest._check_manifest_uri("/uri")
        mock_open.assert_called_with(constants.MANIFEST_CHECK_FILE, 'w')

    @patch("builtins.open", mock.mock_open(read_data="/made-up-URL"), create=True)
    @patch("pyguardian.utils.check_manifest.requests.get", return_value=MockManifestSuccessfulResponse())
    def test_calling_check_manifest_whole_process_unchanged_URI(self, mock_get):
        self.assertIsNone(self.check_manifest())

    @patch("builtins.open", mock.mock_open(read_data="/made-up-URL"), create=True)
    @patch("pyguardian.utils.check_manifest.requests.get", return_value=MockManifestSuccessfulResponseNewURI())
    def test_calling_check_manifest_whole_process_new_URI(self, mock_get):
        self.assertEqual(self.check_manifest(), "/shiny-new-uri")
