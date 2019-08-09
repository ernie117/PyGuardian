import io
from unittest import TestCase
from unittest.mock import patch

from pyguardian.main import destiny_cli
from pyguardian.tests.resources.test_constants import FETCH_STATS_MOCK_RESP, FETCH_EQ_MOCK_RESP


class TestDestinyCLI(TestCase):

    def setUp(self):
        self.parser = destiny_cli.create_parser()

    def test_parser_called_with_full_command(self):
        args = self.parser.parse_args(["ernie", "pc", "stats"])

        self.assertTrue(args.response)
        self.assertTrue(args.guardian)
        self.assertTrue(args.platform)

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
