from unittest import TestCase
from InputValidator import InputValidator

import PyGuardian_Exceptions


class TestInputValidator(TestCase):
    def test_validate_valid_input(self):
        test_guardian, test_platform = "player#22462", "pc"
        result = InputValidator.validate(test_guardian, test_platform)
        assert result, "Should be valid"

    def test_validate_invalid_input_reserved_chars(self):
        test_guardian, test_platform = "player&", "pc"
        self.assertRaises(PyGuardian_Exceptions.PlayerException,
                          InputValidator.validate, test_guardian, test_platform)

    def test_validate_invalid_input_unsafe_chars(self):
        test_guardian, test_platform = "player|", "pc"
        self.assertRaises(PyGuardian_Exceptions.PlayerException,
                          InputValidator.validate, test_guardian, test_platform)

    def test_validate_name_startswith_number_PSN_XBOX(self):
        test_guardian, test_platform = "1player", "playstation"
        self.assertRaises(PyGuardian_Exceptions.PlayerException,
                          InputValidator.validate, test_guardian, test_platform)
        test_platform = "xbox"
        self.assertRaises(PyGuardian_Exceptions.PlayerException,
                          InputValidator.validate, test_guardian, test_platform)

    def test_validate_platform_invalid_platform(self):
        test_guardian, test_platform = "player", "atari"
        self.assertRaises(PyGuardian_Exceptions.PlatformException,
                          InputValidator.validate, test_guardian, test_platform)
    
    def test_validate_platform_platform_as_number(self):
        test_guardian, test_platform = "player", "123"
        self.assertRaises(PyGuardian_Exceptions.PlatformException,
                          InputValidator.validate, test_guardian, test_platform)
