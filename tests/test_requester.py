import logging
from unittest import TestCase
from unittest.mock import patch

from pyguardian.main.requester import Requester, APIUnavailableException
from pyguardian.tests.resources.mock_classes import MockSearchDestinyPlayerSuccessfulResponse, \
    MockSearchDestinyPlayerUnsuccessfulResponse, MockSearchDestinyPlayerNoSuchPlayer, \
    MockSuccessfulCharacterDataRequest, MockUnsuccessfulCharacterDataRequest, \
    MockSuccessfulCharacterEquipmentDataRequest, MockSuccessfulVaultDataRequest
from pyguardian.validation.pyguardian_exceptions import APIException, PlayerNotFoundException


class TestRequester(TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(level=logging.CRITICAL)
        cls.test_gamertag = "ernie"
        cls.test_platform = "playstation"

    def setUpRequester(self):
        return Requester(self.test_gamertag, self.test_platform)

    @patch("pyguardian.main.requester.requests.get", return_value=MockSearchDestinyPlayerSuccessfulResponse())
    def test_requester_successful_response(self, mock_get):
        requester = self.setUpRequester()

        self.assertEqual(requester.character_equip_url,
                         "https://www.bungie.net/Platform/Destiny2/playstation/" +
                         "Profile/1234567890987654321/?components=205")
        self.assertEqual(requester.character_info_url,
                         "https://www.bungie.net/Platform/Destiny2/playstation/" +
                         "Profile/1234567890987654321/?components=200")
        self.assertEqual(requester.vault_info_url,
                         "https://www.bungie.net/Platform/Destiny2/playstation/" +
                         "Profile/1234567890987654321/?components=102")

    @patch("pyguardian.main.requester.requests.get", return_value=MockSearchDestinyPlayerNoSuchPlayer())
    def test_requester_no_such_player(self, mock_get):
        with self.assertRaises(PlayerNotFoundException):
            self.setUpRequester()

    @patch("pyguardian.main.requester.requests.get", side_effect=(MockSearchDestinyPlayerSuccessfulResponse(),
                                                                  MockSuccessfulCharacterDataRequest()))
    def test_requester_successful_character_data_request(self, mock_get):
        requester = self.setUpRequester()
        char_info = requester.fetch_character_info()

        self.assertTrue(char_info)
        self.assertIsInstance(char_info, dict)
        self.assertEqual(char_info["Response"]["characters"]["data"]["1234567890123456789"]["light"],
                         731)
        self.assertIsInstance(char_info["Response"]["characters"]["data"]["1234567890123456789"]["stats"],
                              dict)

    @patch("pyguardian.main.requester.requests.get", side_effect=(MockSearchDestinyPlayerSuccessfulResponse(),
                                                                  MockUnsuccessfulCharacterDataRequest()))
    def test_requester_unsuccessful_character_data_request(self, mock_get):
        requester = self.setUpRequester()
        char_info = requester.fetch_character_info()

        self.assertIsInstance(char_info, dict)
        self.assertFalse(char_info["Response"])

    @patch("pyguardian.main.requester.requests.get", side_effect=(MockSearchDestinyPlayerSuccessfulResponse(),
                                                                  MockSuccessfulCharacterEquipmentDataRequest()))
    def test_requester_successful_character_equipment_data_request(self, mock_get):
        requester = self.setUpRequester()
        char_equip_info = requester.fetch_character_equip_info()

        self.assertTrue(char_equip_info)
        self.assertIsInstance(char_equip_info, dict)
        self.assertIsInstance(
            char_equip_info["Response"]["characterEquipment"]["data"]["1234567890123456789"]["items"],
            list
        )
        self.assertEqual(
            char_equip_info["Response"]["characterEquipment"]["data"]["1234567890123456789"]["items"][0]["itemHash"],
            2712244741
        )

    @patch("pyguardian.main.requester.requests.get", side_effect=(MockSearchDestinyPlayerSuccessfulResponse(),
                                                                  MockSuccessfulVaultDataRequest()))
    def test_requester_successful_vault_data_request(self, mock_get):
        requester = self.setUpRequester()
        vault_info = requester.fetch_vault_info()

        self.assertTrue(vault_info)
        self.assertIsInstance(vault_info, dict)
        self.assertIsInstance(vault_info["Response"]["profileInventory"]["data"]["items"],
                              list)
        self.assertEqual(vault_info["Response"]["profileInventory"]["data"]["items"][0]["itemHash"],
                         4285666432)
