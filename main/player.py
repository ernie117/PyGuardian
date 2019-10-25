import os
import logging

from pyguardian.main.requester import Requester
from pyguardian.validation.guardian_processor import GuardianProcessor


logging.disable(level=logging.CRITICAL)


class Player:

    def __init__(self):
        self.X_API_KEY = None
        self.PLAYER = None
        self.PLATFORM = None
        self.CHARACTER_JSON = None
        self.VAULT_JSON = None
        self.EQUIPMENT_JSON = None
        self.HISTORICAL_STATS = None

    def api_key(self, api_key):
        self.X_API_KEY = api_key
        return self

    def gamertag(self, gamertag=""):
        self.PLAYER = GuardianProcessor.process_guardian(gamertag)
        return self

    def platform(self, platform=""):
        if not platform:
            return self

        self.PLATFORM = GuardianProcessor.process_platform(platform)
        return self

    def _default_fetch_json(self, arbitrary_request):
        if not self.PLAYER:
            print("Gamertag not set!")
            return
        if not self.PLATFORM:
            print("Platform not set!")
            return

        requester = Requester(self.PLAYER, self.PLATFORM)
        request_dict = {
            "character": requester.fetch_character_info,
            "vault": requester.fetch_vault_info,
            "eq": requester.fetch_character_equip_info,
            "stats": requester.fetch_historical_stats
        }

        key = os.getenv("BUNGIE_API") if os.getenv("BUNGIE_API") is not None else self.X_API_KEY

        return request_dict[arbitrary_request](_headers={"X-API-Key": key})

    def fetch_character_json(self):
        self.CHARACTER_JSON = self._default_fetch_json("character")
        return self.CHARACTER_JSON

    def fetch_vault_json(self):
        self.VAULT_JSON = self._default_fetch_json("vault")
        return self.VAULT_JSON

    def fetch_equipment_json(self):
        self.EQUIPMENT_JSON = self._default_fetch_json("eq")
        return self.EQUIPMENT_JSON

    def fetch_historical_stats(self):
        self.HISTORICAL_STATS = self._default_fetch_json("stats")
        return self.HISTORICAL_STATS

