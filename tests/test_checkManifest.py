import logging
from unittest import TestCase, mock
from unittest.mock import patch

from pyguardian.tests.resources.mock_classes import MockManifestSuccessfulResponse, \
    MockManifestSuccessfulResponseNewURI, \
    MockManifestUnsuccessfulResponse
from pyguardian.utils import constants
from pyguardian.utils.check_manifest import CheckManifest
from pyguardian.validation.pyguardian_exceptions import APIUnavailableException


logging.disable()


class TestCheckManifest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.check_manifest = CheckManifest()

    @patch("pyguardian.utils.check_manifest.requests.get")
    def test_get_manifest_url_returns_nested_URL(self, mock_get):
        mock_get.return_value = MockManifestSuccessfulResponse()
        response = mock_get.return_value.json()

        self.assertEqual(self.check_manifest._get_manifest_uri(),
                         response["Response"]["mobileWorldContentPaths"]["en"])

    @patch("pyguardian.utils.check_manifest.requests.get")
    def test_get_manifest_url_API_down_raises_exception(self, mock_get):
        mock_get.return_value = MockManifestUnsuccessfulResponse()

        self.assertRaises(APIUnavailableException,
                          self.check_manifest._get_manifest_uri)

    @patch("builtins.open", mock.mock_open(read_data="/unique-uri"), create=True)
    def test_check_manifest_url_returns_None_for_unchanged_URI(self):
        self.assertIsNone(self.check_manifest._check_manifest_uri("/unique-uri"))

    @patch("builtins.open", mock.mock_open(read_data="/old-uri"), create=True)
    def test_check_manifest_url_returns_URI_if_new(self):
        self.assertEqual(self.check_manifest._check_manifest_uri("/new-uri"),
                         "/new-uri")

    @patch("builtins.open")
    @patch("os.path.isfile")
    def test_check_manifest_url_creates_new_file_if_no_check_file_found(self, mock_isfile, mock_open):
        mock_isfile.return_value = False
        self.check_manifest._check_manifest_uri("/uri")
        mock_open.assert_called_with(constants.MANIFEST_CHECK_FILE, 'w')

    @patch("pyguardian.utils.check_manifest.requests.get")
    @patch("builtins.open", mock.mock_open(read_data="/made-up-URL"), create=True)
    def test_calling_check_manifest_whole_process_unchanged_URI(self, mock_get):
        mock_get.return_value = MockManifestSuccessfulResponse()

        self.assertIsNone(self.check_manifest())

    @patch("pyguardian.utils.check_manifest.requests.get")
    @patch("builtins.open", mock.mock_open(read_data="/made-up-URL"), create=True)
    def test_calling_check_manifest_whole_process_new_URI(self, mock_get):
        mock_get.return_value = MockManifestSuccessfulResponseNewURI()

        self.assertEqual(self.check_manifest(), "/shiny-new-uri")
