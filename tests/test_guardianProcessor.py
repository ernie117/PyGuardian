from unittest import TestCase

from pyguardian.validation.guardian_processor import GuardianProcessor


class TestGuardianProcessor(TestCase):

    def test_guardian_processor_returns_processed_player_name(self):
        processed_results = GuardianProcessor.process("ernie#909090", "pc")

        self.assertEqual(processed_results[0], "ernie%23909090")

    def test_guardian_processor_returns_correct_platform_number_pc(self):
        processed_results = GuardianProcessor.process("ernie", "pc")

        self.assertEqual(processed_results[1], "3")

    def test_guardian_processor_returns_player_name_without_whitespace(self):
        processed_results = GuardianProcessor.process("   ernie  ", "pc     ")

        self.assertEqual(processed_results, ("ernie", "3"))

    def test_guardian_processor_returns_correct_platform_number_playstation(self):
        processed_results = GuardianProcessor.process("ernie", "playstation")

        self.assertEqual(processed_results[1], "2")

    def test_guardian_processor_returns_correct_platform_number_xbox(self):
        processed_results = GuardianProcessor.process("ernie", "xbox")

        self.assertEqual(processed_results[1], "1")

    def test_guardian_processor_returns_correct_platform_with_uppercase_input(self):
        processed_results = GuardianProcessor.process("ernie", "PLAYSTATION")

        self.assertEqual(processed_results[1], "2")

    def test_guardian_processor_returns_correct_with_whitespace_octothorpe_and_uppercase_input(self):
        processed_results = GuardianProcessor.process(" ernie#22462   ", "     PLAYSTATION ")

        self.assertEqual(processed_results, ("ernie%2322462", "2"))
