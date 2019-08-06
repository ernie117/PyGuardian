import json
from unittest import TestCase

from pyguardian.data_processing.json_funcs import *
from pyguardian.tests.resources import test_constants


class TestJsonFuncs(TestCase):

    @classmethod
    def setUpClass(cls):
        with open(test_constants.TEST_CHAR_DATA) as f:
            cls.char_data = json.load(f)
        with open(test_constants.TEST_EQUIP_DATA) as f:
            cls.equip_data = json.load(f)
        with open(test_constants.TEST_VAULT_DATA) as f:
            cls.vault_data = json.load(f)

        cls.expected_eq_hashes_char_one = test_constants.EXPECTED_EQ_HASHES_CHAR_ONE
        cls.expected_eq_hashes_char_two = test_constants.EXPECTED_EQ_HASHES_CHAR_TWO
        cls.expected_char_info_keys = test_constants.EXPECTED_CHAR_INFO_KEYS
        cls.expected_last_played_keys = test_constants.EXPECTED_LAST_PLAYED_KEYS
        cls.expected_play_time_keys = test_constants.EXPECTED_PLAY_TIME_KEYS
        cls.expected_vault_hashes = test_constants.EXPECTED_VAULT_HASHES

    def test_fetch_eq_hashes_returns_expected_data(self):
        eq_hashes = fetch_eq_hashes(self.equip_data, self.char_data)

        self.assertTrue(eq_hashes)
        self.assertEqual(2, len(eq_hashes))
        self.assertIsInstance(eq_hashes, list)

        self.assertIn(self.expected_eq_hashes_char_one, eq_hashes)
        self.assertIn(self.expected_eq_hashes_char_two, eq_hashes)

    def test_fetch_char_info_returns_expected_data(self):
        char_info = fetch_char_info(self.char_data)

        self.assertTrue(char_info)
        self.assertEqual(2, len(char_info))
        self.assertIsInstance(char_info, list)
        self.assertIsInstance(char_info[0], dict)
        self.assertIsInstance(char_info[1], dict)

        self.assertEqual(self.expected_char_info_keys, list(char_info[0].keys()))

        self.assertEqual(char_info[0]["Power"], 731)
        self.assertEqual(char_info[1]["Level"], 50)

    def test_fetch_last_time_played_returns_expected_data(self):
        times = fetch_last_time_played(self.char_data)

        self.assertTrue(times)
        self.assertEqual(2, len(times))
        self.assertIsInstance(times, list)
        self.assertIsInstance(times[0], dict)
        self.assertIsInstance(times[1], dict)

        self.assertEqual(self.expected_last_played_keys, list(times[0].keys()))

        self.assertEqual(times[0]["Datetime"], "00:00:00 -- Fri 01/03")
        self.assertEqual(times[1]["Datetime"], "00:00:00 -- Thu 07/03")

    def test_fetch_play_time_returns_expected_data(self):
        times = fetch_play_time(self.char_data)

        self.assertTrue(times)
        self.assertEqual(3, len(times))
        self.assertIsInstance(times, list)
        self.assertIsInstance(times[0], dict)
        self.assertIsInstance(times[1], dict)
        self.assertIsInstance(times[2], dict)

        self.assertEqual(self.expected_play_time_keys, list(times[0].keys()))

        self.assertEqual(times[0]["Time"], "1100h 0m")
        self.assertEqual(times[1]["Time"], "66h 40m")

    def test_fetch_vault_hashes_returns_expected_data(self):
        hashes = fetch_vault_hashes(self.vault_data)

        self.assertTrue(hashes)
        self.assertIsInstance(hashes, list)
        self.assertIsInstance(hashes[0], list)

        self.assertEqual(self.expected_vault_hashes, hashes[0])

    def test_fetch_eq_hashes_raises_correct_exceptions(self):
        self.assertRaises(PlayerNotFoundException,
                          fetch_eq_hashes, self.equip_data, {})

        self.assertRaises(NoPlayerEquipmentException,
                          fetch_eq_hashes, {}, self.char_data)

    def test_fetch_char_info_raises_correct_exception(self):
        self.assertRaises(PlayerNotFoundException,
                          fetch_char_info, {})

    def test_fetch_last_time_played_raises_correct_exception(self):
        self.assertRaises(PlayerNotFoundException,
                          fetch_last_time_played, {})

    def test_fetch_play_time_raises_correct_exception(self):
        self.assertRaises(PlayerNotFoundException,
                          fetch_play_time, {})

    def test_vault_hashes_raises_correct_exception(self):
        self.assertRaises(VaultAccessBlockedException,
                          fetch_vault_hashes, {})

    def test_json_miner_returns_expected_dict_type(self):
        characters = json_miner("Response.characters.data", self.char_data)

        self.assertTrue(characters)
        self.assertIsInstance(characters, dict)

        self.assertIn("1234567890123456789", characters)
        self.assertIn("2345678901234567889", characters)

    def test_json_mireturns_expected_list_type(self):
        list_element = json_miner("Response.characterEquipment.data.1234567890123456789.items",
                                  self.equip_data)

        self.assertTrue(list_element)
        self.assertIsInstance(list_element, list)
        self.assertIsInstance(list_element[0], dict)

        dict_inside_list = json_miner("0", list_element)

        self.assertIsInstance(dict_inside_list, dict)
        self.assertIn(2712244741, dict_inside_list.values())

        second_dict_inside_list = json_miner("1", list_element)

        self.assertIsInstance(dict_inside_list, dict)
        self.assertIn(1887808042, second_dict_inside_list.values())
