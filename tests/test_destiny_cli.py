import io
from unittest import TestCase, mock
from unittest.mock import patch

from pyguardian.main import destiny_cli
from pyguardian.tests.resources.mock_classes import MockCheckManifest, MockGetManifest, MockCheckManifestReturnNone
from pyguardian.tests.resources.test_constants import FETCH_STATS_MOCK_RESP, FETCH_EQ_MOCK_RESP, FETCH_VAULT_MOCK_RESP,\
    FETCH_PLAYTIME_MOCK_RESP, FETCH_LAST_PLAY_MOCK_RESP


class TestDestinyCLI(TestCase):

    def setUp(self):
        self.parser = destiny_cli.create_parser()

    def test_parser_called_with_full_arguments(self):
        args = self.parser.parse_args(["ernie", "pc", "stats"])

        self.assertTrue(args.guardian)
        self.assertTrue(args.platform)
        self.assertTrue(args.response)

    def test_parser_called_with_one_argument(self):
        args = self.parser.parse_args(["ernie"])

        self.assertTrue(args.guardian)
        self.assertFalse(args.platform)
        self.assertFalse(args.response)

    def test_parser_called_with_two_arguments(self):
        args = self.parser.parse_args(["ernie", "pc"])

        self.assertTrue(args.guardian)
        self.assertTrue(args.platform)
        self.assertFalse(args.response)

    @patch("pyguardian.main.destiny_cli.PyGuardian.fetch_stats")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_destiny_cli_main_fetch_stats(self, mock_stdout, mock_pyguardian):
        mock_pyguardian.return_value = FETCH_STATS_MOCK_RESP
        destiny_cli.main(["ernie", "pc", "stats"])

        mock_pyguardian.assert_called_once()
        self.assertEqual(mock_stdout.getvalue().strip(),
                         "│ Character │ Power │ Mobility │  Resilience │ Recovery │  Level │")

    @patch("pyguardian.main.destiny_cli.PyGuardian.fetch_eq")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_destiny_cli_main_fetch_eq(self, mock_stdout, mock_pyguardian):
        mock_pyguardian.return_value = FETCH_EQ_MOCK_RESP
        destiny_cli.main(["ernie", "playstation", "eq"])

        mock_pyguardian.assert_called_once()
        self.assertEqual(mock_stdout.getvalue().strip(),
                         "│ MALE │ EXO │ WARLOCK │")

    @patch("pyguardian.main.destiny_cli.PyGuardian.fetch_vault")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_destiny_cli_main_fetch_vault(self, mock_stdout, mock_pyguardian):
        mock_pyguardian.return_value = FETCH_VAULT_MOCK_RESP
        destiny_cli.main(["ernie", "playstation", "vault"])

        mock_pyguardian.assert_called_once()
        self.assertEqual(mock_stdout.getvalue().strip(),
                         "│ Item Name │ Item Type │ Item Tier │")

    @patch("pyguardian.main.destiny_cli.PyGuardian.fetch_vault")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_destiny_cli_main_fetch_vault_sort_name(self, mock_stdout, mock_pyguardian):
        mock_pyguardian.return_value = FETCH_VAULT_MOCK_RESP
        destiny_cli.main(["ernie", "playstation", "vault-name"])

        mock_pyguardian.assert_called_once_with("ernie", "playstation", sort="name")
        self.assertEqual(mock_stdout.getvalue().strip(),
                         "│ Item Name │ Item Type │ Item Tier │")

    @patch("pyguardian.main.destiny_cli.PyGuardian.fetch_vault")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_destiny_cli_main_fetch_vault_sort_type(self, mock_stdout, mock_pyguardian):
        mock_pyguardian.return_value = FETCH_VAULT_MOCK_RESP
        destiny_cli.main(["ernie", "playstation", "vault-type"])

        mock_pyguardian.assert_called_once_with("ernie", "playstation", sort="type")
        self.assertEqual(mock_stdout.getvalue().strip(),
                         "│ Item Name │ Item Type │ Item Tier │")

    @patch("pyguardian.main.destiny_cli.PyGuardian.fetch_vault")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_destiny_cli_main_fetch_vault_sort_tier(self, mock_stdout, mock_pyguardian):
        mock_pyguardian.return_value = FETCH_VAULT_MOCK_RESP
        destiny_cli.main(["ernie", "playstation", "vault-tier"])

        mock_pyguardian.assert_called_once_with("ernie", "playstation", sort="tier")
        self.assertEqual(mock_stdout.getvalue().strip(),
                         "│ Item Name │ Item Type │ Item Tier │")

    @patch("pyguardian.main.destiny_cli.PyGuardian.fetch_playtime")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_destiny_cli_main_fetch_playtime(self, mock_stdout, mock_pyguardian):
        mock_pyguardian.return_value = FETCH_PLAYTIME_MOCK_RESP
        destiny_cli.main(["ernie", "playstation", "playtime"])

        mock_pyguardian.assert_called_once()
        self.assertEqual(mock_stdout.getvalue().strip(),
                         "│ Character │ Time │")

    @patch("pyguardian.main.destiny_cli.PyGuardian.fetch_last_time_played")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_destiny_cli_main_fetch_last_play_time(self, mock_stdout, mock_pyguardian):
        mock_pyguardian.return_value = FETCH_LAST_PLAY_MOCK_RESP
        destiny_cli.main(["ernie", "playstation", "last"])

        mock_pyguardian.assert_called_once()
        self.assertEqual(mock_stdout.getvalue().strip(),
                         "│ Character │ Datetime │ Session │")

    @patch("pyguardian.main.destiny_cli.CheckManifest")
    @patch("pyguardian.main.destiny_cli.GetManifest")
    def test_destiny_cli_download_manifest(self, mock_get_manifest, mock_check_manifest):
        mock_check_manifest.return_value = MockCheckManifest()
        mock_get_manifest.return_value = MockGetManifest()
        destiny_cli.main(["-d"])
        mock_check_manifest.assert_called_once()
        mock_get_manifest.assert_called_once()

    @patch("pyguardian.main.destiny_cli.CheckManifest")
    @patch("pyguardian.main.destiny_cli.GetManifest")
    def test_destiny_cli_download_manifest_not_required(self, mock_get_manifest, mock_check_manifest):
        mock_check_manifest.return_value = MockCheckManifestReturnNone()
        destiny_cli.main(["-d"])
        mock_check_manifest.assert_called_once()
        mock_get_manifest.assert_not_called()

    @patch("pyguardian.main.destiny_cli.logging.disable")
    def test_destiny_cli_logging_re_enabled_if_logging_argument_passed(self, mock_log):
        destiny_cli.main(["--log"])
        mock_log.assert_has_calls([mock.call(), mock.call(0)])

    @patch("pyguardian.main.destiny_cli.logging.disable")
    def test_destiny_cli_logging_not_enabled_if_logging_argument_not_passed(self, mock_log):
        destiny_cli.main([])
        mock_log.assert_called_once_with()
