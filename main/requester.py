import requests

from pyguardian.utils import constants
from pyguardian.utils.pyguardian_decorators import log_me
from pyguardian.utils.pyguardian_logging import PyGuardianLogger
from pyguardian.validation.pyguardian_exceptions import *


class Requester:
    HEADERS = {"X-API-Key": constants.BUNGIE_API_KEY}
    LOGGER = PyGuardianLogger("Requester.py")

    def __init__(self, gamertag, platform):

        self.player_name = gamertag
        self.platform = platform
        self.character_info_url = None
        self.vault_info_url = None
        self.character_equip_url = None
        self.mem_id = None

    @log_me
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
            self.LOGGER.warn("No membershipId for this player")
            raise PlayerNotFoundException("Can't find that player")

        self.LOGGER.info(f"Player '{self.player_name}' found \u2713")

        urls = [constants.BASE
                + self.platform
                + "/Profile/"
                + self.mem_id
                + "/?components="
                + component for component in constants.COMPONENTS]

        self.character_info_url = urls[0]
        self.vault_info_url = urls[1]
        self.character_equip_url = urls[2]

    @log_me
    def fetch_character_info(self):

        return requests.get(self.character_info_url, headers=self.HEADERS).json()

    @log_me
    def fetch_vault_info(self):

        return requests.get(self.vault_info_url, headers=self.HEADERS).json()

    @log_me
    def fetch_character_equip_info(self):

        return requests.get(self.character_equip_url, headers=self.HEADERS).json()
