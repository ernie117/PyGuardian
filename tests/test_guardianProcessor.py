from unittest import TestCase

from pyguardian.validation.guardian_processor import GuardianProcessor


class TestGuardianProcessor(TestCase):

    def test_guardian_processor_returns_processed_player_name(self):
        processed_results = GuardianProcessor.process("ernie#909090", "pc")

        self.assertEqual(processed_results[0], "ernie%23909090")

    def test_guardian_processor_returns_processed_platform(self):
        processed_results = GuardianProcessor.process("ernie", "pc")

        self.assertEqual(processed_results[1], "4")

