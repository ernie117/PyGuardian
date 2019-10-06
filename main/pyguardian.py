"""
This facade class holds a collection of methods that offload all
the heavy lifting of requesting and processing to other modules

This class can also be instantiated and used as a fluent interface,
gamertag and platform can be used to call further methods to request
character data or equipment json data for the user's own needs
"""
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
from pyguardian.validation.pyguardian_exceptions import *


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

        try:
            guardian, platform = PyGuardian.prechecks(guardian, platform)
            account = Requester(guardian, platform)
            char_data = account.fetch_character_info()
            equip_data = account.fetch_character_equip_info()
            weapon_hashes = json_funcs.fetch_eq_hashes(equip_data, char_data)
            weapon_data = InventoryManifest(weapon_hashes)
            return weapon_data.get_full_item_details()

        except (APIException, APIUnavailableException) as ape:
            logger = PyGuardianLogger()
            logger.error(ape)
        finally:
            logging.shutdown()

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
    def fetch_pvp_info(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        char_data = account.fetch_character_info()
        historical_stats = account.fetch_historical_stats()
        return json_funcs.fetch_kd(historical_stats, char_data)

    @staticmethod
    def get_guardian_objects(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        char_data = account.fetch_character_info()
        equip_data = account.fetch_character_equip_info()
        equipment_details = json_funcs.fetch_character_eq_details(equip_data, char_data)
        char_data = json_funcs.fetch_extended_char_info(char_data, equipment_details, guardian)
        return json_funcs.get_data_guardian_objects(char_data, equipment_details)

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

            uri = check_manifest()
            if uri is not None:
                get_manifest(uri)

        except OSError:
            log.error("Can't create directories!")
            raise CannotCreateStorageDirectories()

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
