import json
from pathlib import Path
from unittest import TestCase

from pyguardian.data_processing.json_funcs import *


class TestJsonFuncs(TestCase):

    # Reading in the dummy test data
    with open(str(Path(__file__).parent) + "/resources/dummy_character_data.json", "r") as f:
        char_data = json.load(f)
    with open(str(Path(__file__).parent) + "/resources/dummy_equip_data.json", "r") as f:
        equip_data = json.load(f)
    with open(str(Path(__file__).parent) + "/resources/dummy_vault_data.json", "r") as f:
        vault_data = json.load(f)

    expected_char_info_keys = ["Character", "Power", "Mobility", "Resilience", "Recovery", "Level"]
    expected_last_played_keys = ["Character", "Datetime", "Session"]
    expected_play_time_keys = ["Character", "Time"]

    expected_eq_hashes_char_one = [
        ["MALE", "EXO", "WARLOCK"],
        2712244741, 1887808042,
        1201830623, 381563628,
        3830828709, 3192591867,
        4178158375, 1549308050,
        813936739, 1363029408,
        2844014413
    ]

    expected_eq_hashes_char_two = [
        ["MALE", "HUMAN", "TITAN"],
        1457394911, 1678957659,
        1877183765, 1070180272,
        809007411, 201644247,
        2362809459, 2329963686,
        3717471208, 2351197433,
        682682138
    ]

    expected_vault_hashes = [
        4285666432, 2014411539, 4101386442, 1177810185, 2109561326, 950899352
    ]

    def test_fetch_eq_hashes(self):
        """
        fetch_eq_hashes returns a list of lists of hash codes of character
        equipment, plus a list of traits describing the character
        """
        eq_hashes = fetch_eq_hashes(self.equip_data, self.char_data)

        self.assertTrue(eq_hashes)
        self.assertEqual(2, len(eq_hashes))
        self.assertIsInstance(eq_hashes, list)

        self.assertIn(self.expected_eq_hashes_char_one, eq_hashes)
        self.assertIn(self.expected_eq_hashes_char_two, eq_hashes)

    def test_fetch_char_info(self):
        """
        fetch_char_info returns a list of dictionaries, each
        containing stats describing the player's characters
        """
        char_info = fetch_char_info(self.char_data)

        self.assertTrue(char_info)
        self.assertEqual(2, len(char_info))
        self.assertIsInstance(char_info, list)
        self.assertIsInstance(char_info[0], dict)
        self.assertIsInstance(char_info[1], dict)

        self.assertEquals(self.expected_char_info_keys, list(char_info[0].keys()))

        self.assertEqual(char_info[0]["Power"], 731)
        self.assertEqual(char_info[1]["Level"], 50)

    def test_fetch_last_time_played(self):
        """
        fetch_last_time_played returns a list of dictionaries,
        each containing total time spent on game characters
        """
        times = fetch_last_time_played(self.char_data)

        self.assertTrue(times)
        self.assertEqual(2, len(times))
        self.assertIsInstance(times, list)
        self.assertIsInstance(times[0], dict)
        self.assertIsInstance(times[1], dict)

        self.assertEquals(self.expected_last_played_keys, list(times[0].keys()))

        self.assertEqual(times[0]["Datetime"], "00:00:00 -- Fri 01/03")
        self.assertEqual(times[1]["Datetime"], "00:00:00 -- Thu 07/03")

    def test_fetch_play_time(self):
        """
        fetch_play_time returns a list of dictionaries
        containing character descriptions and total time
        played on each, plus a dict acting as a total
        count of time played over all characters
        """
        times = fetch_play_time(self.char_data)

        self.assertTrue(times)
        self.assertEqual(3, len(times))
        self.assertIsInstance(times, list)
        self.assertIsInstance(times[0], dict)
        self.assertIsInstance(times[1], dict)
        self.assertIsInstance(times[2], dict)

        self.assertEquals(self.expected_play_time_keys, list(times[0].keys()))

        self.assertEqual(times[0]["Time"], "1100h 0m")
        self.assertEqual(times[1]["Time"], "66h 40m")

    def test_fetch_vault_hashes(self):
        """
        fetch_vault_hashes returns a list of lists of hashes
        representing items like weapons and armour present in
        the player's vault
        """
        hashes = fetch_vault_hashes(self.vault_data)

        self.assertTrue(hashes)
        self.assertIsInstance(hashes, list)
        self.assertIsInstance(hashes[0], list)

        self.assertEquals(self.expected_vault_hashes, hashes[0])


