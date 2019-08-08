from unittest import TestCase

from pyguardian.validation import pyguardian_exceptions
from pyguardian.validation.input_validator import InputValidator


class TestInputValidator(TestCase):

    def test_validate_valid_input(self):
        test_guardian, test_platform = "player#22462", "pc"
        result = InputValidator.validate(test_guardian, test_platform)
        self.assertTrue(result), "Should be valid"

    def test_validate_invalid_input_reserved_chars(self):
        test_guardian, test_platform = "player&", "pc"
        self.assertRaises(pyguardian_exceptions.PlayerException,
                          InputValidator.validate, test_guardian, test_platform)

    def test_validate_invalid_input_unsafe_chars(self):
        test_guardian, test_platform = "player|", "pc"
        self.assertRaises(pyguardian_exceptions.PlayerException,
                          InputValidator.validate, test_guardian, test_platform)

    def test_validate_name_startswith_number_PSN_XBOX(self):
        test_guardian, test_platform = "1player", "playstation"
        self.assertRaises(pyguardian_exceptions.PlayerException,
                          InputValidator.validate, test_guardian, test_platform)
        test_platform = "xbox"
        self.assertRaises(pyguardian_exceptions.PlayerException,
                          InputValidator.validate, test_guardian, test_platform)

    def test_validate_platform_valid_platforms(self):
        valid_platforms = ["xbox", "playstation", "pc"]
        test_guardian = "player"
        for platform in valid_platforms:
            self.assertTrue(InputValidator.validate(test_guardian, platform))

    def test_validate_platform_invalid_platform(self):
        test_guardian, test_platform = "player", "atari"
        self.assertRaises(pyguardian_exceptions.PlatformException,
                          InputValidator.validate, test_guardian, test_platform)
    
    def test_validate_platform_platform_as_number(self):
        test_guardian, test_platform = "player", "123"
        self.assertRaises(pyguardian_exceptions.PlatformException,
                          InputValidator.validate, test_guardian, test_platform)

    def test_validate_validate_platform_is_valid_platform(self):
        test_platform = "genesis"
        self.assertRaises(pyguardian_exceptions.PlatformException,
                          InputValidator.validate_platform_is_valid_platform, test_platform)

    def test_validate_validate_platform_is_not_all_digits(self):
        test_platform = "123"
        self.assertRaises(pyguardian_exceptions.PlatformException,
                          InputValidator.validate_platform_is_not_digits, test_platform)
