"""
This facade class holds a collection of methods that offload all
the heavy lifting of requesting and processing to other modules
"""
import json
import logging
import os
from pathlib import Path

from pyguardian.data_processing import json_funcs
from pyguardian.data_processing.get_manifest import GetManifest
from pyguardian.data_processing.hashes import InventoryManifest
from pyguardian.main.requester import Requester
from pyguardian.utils import constants
from pyguardian.utils.check_manifest import CheckManifest
from pyguardian.utils.pyguardian_decorators import tabulate_me, log_me
from pyguardian.utils.pyguardian_logging import PyGuardianLogger
from pyguardian.validation.guardian_processor import GuardianProcessor
from pyguardian.validation.input_validator import InputValidator
from pyguardian.validation.pyguardian_exceptions import CannotCreateStorageDirectories


class PyGuardian:

    logging.disable(level=logging.CRITICAL)

    @staticmethod
    @tabulate_me
    @log_me
    def fetch_stats(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        response = account.fetch_character_info()
        return json_funcs.fetch_char_info(response)

    @staticmethod
    @tabulate_me
    @log_me
    def fetch_eq(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        char_data = account.fetch_character_info()
        equip_data = account.fetch_character_equip_info()
        weapon_hashes = json_funcs.fetch_eq_hashes(equip_data, char_data)
        weapon_data = InventoryManifest(weapon_hashes)
        return weapon_data.get_full_item_details()

    @staticmethod
    @tabulate_me
    @log_me
    def fetch_vault(guardian, platform, sort=None):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        vault_data = account.fetch_vault_info()
        vault_hashes = json_funcs.fetch_vault_hashes(vault_data)
        vault_items = InventoryManifest(vault_hashes)
        return vault_items.get_full_item_details(sort_by=sort)

    @staticmethod
    @tabulate_me
    @log_me
    def fetch_playtime(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        char_data = account.fetch_character_info()
        return json_funcs.fetch_play_time(char_data)

    @staticmethod
    @tabulate_me
    @log_me
    def fetch_last_time_played(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        char_data = account.fetch_character_info()
        return json_funcs.fetch_last_time_played(char_data)

    @staticmethod
    @tabulate_me
    @log_me
    def fetch_kd(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        char_data = account.fetch_character_info()
        historical_stats = account.fetch_historical_stats()
        return json_funcs.fetch_kd(historical_stats, char_data)

    @staticmethod
    def get_guardian_object(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        char_data = account.fetch_character_info()
        equip_data = account.fetch_character_equip_info()
        equipment_details = json_funcs.fetch_character_eq_hashes(equip_data, char_data)
        char_data = json_funcs.fetch_extended_char_info(char_data, equipment_details, guardian)
        return json_funcs.get_data_guardian_object(char_data, equipment_details)


    @staticmethod
    @log_me
    def prechecks(guardian, platform):

        get_manifest = GetManifest()
        check_manifest = CheckManifest()
        log = PyGuardianLogger()
        try:
            if not os.path.isdir(constants.DATA_DIR):
                log.info("Creating data directory")
                os.makedirs(constants.MANIFEST_DIR)
            if not os.path.isdir(constants.MANIFEST_DIR):
                log.info("Creating manifest directory")
                os.makedirs(constants.MANIFEST_DIR)
            if not os.path.isdir(constants.JSON_DIR):
                log.info("Creating JSON directory")
                os.makedirs(constants.JSON_DIR)
            if not os.path.isdir(constants.CHARACTER_JSON_DIR):
                log.info("Creating Character JSON directory")
                os.makedirs(constants.CHARACTER_JSON_DIR)
            if not os.listdir(str(Path.home()) + "/.pyguardian/DDB-Files"):
                log.info("Manifest files not available, requesting...")
                get_manifest(check_manifest())
        except OSError:
            log.error("Can't create directories!")
            raise CannotCreateStorageDirectories()

        uri = check_manifest()
        if uri is not None:
            get_manifest(uri)

        InputValidator.validate(guardian, platform)

        return GuardianProcessor.process(guardian, platform)

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
        return self

    def fetch_vault_json(self):
        self.VAULT_JSON = self._default_fetch_json("vault")
        return self

    def fetch_equipment_json(self):
        self.EQUIPMENT_JSON = self._default_fetch_json("eq")
        return self

    def fetch_historical_stats(self):
        self.HISTORICAL_STATS = self._default_fetch_json("stats")
        return self

    def get_character_json(self):
        return self.CHARACTER_JSON

    def get_vault_json(self):
        return self.VAULT_JSON

    def get_equipment_json(self):
        return self.EQUIPMENT_JSON

    def get_historical_stats_json(self):
        return self.HISTORICAL_STATS

    def print_char_json(self):
        if self.CHARACTER_JSON:
            print(json.dumps(self.CHARACTER_JSON, indent=4))

        return self

    def print_vault_json(self):
        if self.VAULT_JSON:
            print(json.dumps(self.VAULT_JSON, indent=4))

        return self

    def print_eq_json(self):
        if self.EQUIPMENT_JSON:
            print(json.dumps(self.EQUIPMENT_JSON, indent=4))

        return self

    def print_stats_json(self):
        if self.HISTORICAL_STATS:
            print(json.dumps(self.HISTORICAL_STATS, indent=4))

        return self

    def _default_write_json(self, data_to_write, write_dir="."):
        data_dict = {
            "character": self.CHARACTER_JSON,
            "vault": self.VAULT_JSON,
            "eq": self.EQUIPMENT_JSON,
            "stats": self.HISTORICAL_STATS
        }

        if data_dict[data_to_write]:
            filename = write_dir + "/" + self.PLAYER + "-" + data_to_write + "-info.json"
            with open(filename, "w") as f:
                print(f"Writing {data_to_write} JSON to file")
                json.dump(data_dict[data_to_write], f, indent=4)

    def write_char_json(self, write_dir="."):
        if self.CHARACTER_JSON:
            self._default_write_json("character", write_dir)

    def write_vault_json(self, write_dir="."):
        if self.VAULT_JSON:
            self._default_write_json("vault", write_dir)

    def write_eq_json(self, write_dir="."):
        if self.EQUIPMENT_JSON:
            self._default_write_json("eq", write_dir)

    def write_stats_json(self, write_dir="."):
        if self.HISTORICAL_STATS:
            self._default_write_json("stats", write_dir)
