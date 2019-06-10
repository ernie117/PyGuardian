from validation.PyGuardian_Exceptions import *

import requests
from utils import constants


class Requester:

    HEADERS = {"X-API-Key": constants.BUNGIE_API_KEY}

    def __init__(self, gamertag, platform):

        self.player_name = gamertag
        self.platform = platform
        self.character_info_url = None
        self.vault_info_url = None
        self.character_equip_url = None
        self.mem_id = None

    def fetch_player(self):

        r = requests.get(constants.BASE
                         + "SearchDestinyPlayer/"
                         + self.platform
                         + '/'
                         + self.player_name,
                         headers=self.HEADERS).json()

        if r["ErrorStatus"] == "SystemDisabled":
            raise APIException("API is down!")

        try:
            self.mem_id = r["Response"][0]["membershipId"]
        except IndexError:
            raise PlayerNotFoundException("Can't find that player")

        print("Player found \u2713")

        urls = [constants.BASE
                + self.platform
                + "/Profile/"
                + self.mem_id
                + "/?components="
                + component for component in constants.COMPONENTS]

        self.character_info_url = urls[0]
        self.vault_info_url = urls[1]
        self.character_equip_url = urls[2]

    def fetch_character_info(self):

        return requests.get(self.character_info_url, headers=self.HEADERS).json()

    def fetch_vault_info(self):

        return requests.get(self.vault_info_url, headers=self.HEADERS).json()

    def fetch_character_equip_info(self):

        return requests.get(self.character_equip_url, headers=self.HEADERS).json()

