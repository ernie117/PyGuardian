import requests

from pyguardian.utils import constants
from pyguardian.utils.api_status import APIStatusChecker
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
        self.historical_stats_url = None
        self.mem_id = None
        self._fetch_player()

    @log_me
    def _fetch_player(self):

        r = requests.get(constants.BASE
                         + "SearchDestinyPlayer/"
                         + self.platform
                         + '/'
                         + self.player_name,
                         headers=self.HEADERS).json()

        _ = APIStatusChecker(r)

        try:
            self.mem_id = r["Response"][0]["membershipId"]
        except IndexError:
            self.LOGGER.warn("No membershipId for this player")
            raise PlayerNotFoundException("Can't find that player")

        self.LOGGER.info(f"Player '{self.player_name}' found.")

        urls = [constants.BASE
                + self.platform
                + "/Profile/"
                + self.mem_id
                + "/?components="
                + component for component in constants.COMPONENTS]

        historical_stats_url = (
                constants.BASE
                + self.platform
                + "/Account/"
                + self.mem_id
                + "/Stats"
                + "?modes=AllPvP"
        )

        self.character_info_url = urls[0]
        self.vault_info_url = urls[1]
        self.character_equip_url = urls[2]
        self.historical_stats_url = historical_stats_url

    @log_me
    def fetch_character_info(self, _headers=None):

        actual_headers = self.HEADERS if _headers is None else _headers
        return requests.get(self.character_info_url,
                            headers=actual_headers).json()

    @log_me
    def fetch_vault_info(self, _headers=None):

        actual_headers = self.HEADERS if _headers is None else _headers
        return requests.get(self.vault_info_url, headers=actual_headers).json()

    @log_me
    def fetch_character_equip_info(self, _headers=None):

        actual_headers = self.HEADERS if _headers is None else _headers
        return requests.get(self.character_equip_url,
                            headers=actual_headers).json()

    @log_me
    def fetch_historical_stats(self, _headers=None):

        actual_headers = self.HEADERS if _headers is None else _headers
        return requests.get(self.historical_stats_url,
                            headers=actual_headers).json()
