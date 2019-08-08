from unittest import TestCase, mock
from pyguardian.main import destiny_cli


class TestDestinyCLI(TestCase):

    def setUp(self):
        self.parser = destiny_cli.create_parser()

    @mock.patch("builtins.print")
    def test_parser_called_with_stats(self, mock_print):
        args = self.parser.parse_args(["ernie", "pc", "stats"])

        self.assertTrue(args.response)
