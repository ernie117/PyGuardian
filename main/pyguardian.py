"""
This façade class holds a collection of methods that offload all
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

    logging.disable()
    CHARACTER_JSON = None
    EQUIPMENT_JSON = None
    VAULT_JSON = None

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

    def api_key(self, api_key):
        self.X_API_KEY = api_key
        return self

    def gamertag(self, gamertag):
        self.PLAYER = GuardianProcessor.process_guardian(gamertag)
        return self

    def platform(self, platform):
        self.PLATFORM = GuardianProcessor.process_platform(platform)
        return self

    def get_character_json(self):
        key = os.getenv("BUNGIE_API") if os.getenv("BUNGIE_API") is not None else self.X_API_KEY
        self.CHARACTER_JSON = Requester(self.PLAYER, self.PLATFORM) \
            .fetch_character_info(headers={"X-API-Key": key})
        return self

    def get_vault_json(self):
        key = os.getenv("BUNGIE_API") if os.getenv("BUNGIE_API") is not None else self.X_API_KEY
        self.VAULT_JSON = Requester(self.PLAYER, self.PLATFORM) \
            .fetch_vault_info(headers={"X-API-Key": key})
        return self

    def get_equipment_json(self):
        key = os.getenv("BUNGIE_API") if os.getenv("BUNGIE_API") is not None else self.X_API_KEY
        self.EQUIPMENT_JSON = Requester(self.PLAYER, self.PLATFORM) \
            .fetch_character_equip_info(headers={"X-API-Key": key})
        return self

    def print_char_info(self):
        if self.CHARACTER_JSON:
            print(json.dumps(self.CHARACTER_JSON, indent=4))
        else:
            print("No character info json")

    def print_vault_info(self):
        if self.VAULT_JSON:
            print(json.dumps(self.VAULT_JSON, indent=4))
        else:
            print("No vault info json")

    def print_eq_info(self):
        if self.EQUIPMENT_JSON:
            print(json.dumps(self.EQUIPMENT_JSON, indent=4))
        else:
            print("No equipment info json")

    def write_char_json(self):
        if self.CHARACTER_JSON:
            pass

    def write_vault_json(self):
        if self.VAULT_JSON:
            pass

    def write_eq_json(self):
        if self.EQUIPMENT_JSON:
            pass

    def write_all(self):
        pass
