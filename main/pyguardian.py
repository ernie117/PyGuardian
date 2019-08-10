"""
This façade class holds a collection of methods that offload all
the heavy lifting of requesting and processing to other modules
"""
import os
from pathlib import Path

from pyguardian.data_processing import json_funcs
from pyguardian.data_processing.get_manifest import GetManifest
from pyguardian.data_processing.hashes import InventoryManifest
from pyguardian.main.requester import Requester
from pyguardian.utils import constants
from pyguardian.utils.check_manifest import CheckManifest
from pyguardian.utils.pyguardian_decorators import tabulate_me, log_me
from pyguardian.validation.guardian_processor import GuardianProcessor
from pyguardian.validation.input_validator import InputValidator
from pyguardian.validation.pyguardian_exceptions import CannotCreateStorageDirectories


class PyGuardian:

    @staticmethod
    @tabulate_me
    def fetch_stats(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        account.fetch_player()
        response = account.fetch_character_info()
        return json_funcs.fetch_char_info(response)

    @staticmethod
    @tabulate_me
    def fetch_eq(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        account.fetch_player()
        char_data = account.fetch_character_info()
        equip_data = account.fetch_character_equip_info()
        weapon_hashes = json_funcs.fetch_eq_hashes(equip_data, char_data)
        weapon_data = InventoryManifest(weapon_hashes)
        return weapon_data.get_full_item_details()

    @staticmethod
    @tabulate_me
    def fetch_vault(guardian, platform, sort=None):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        account.fetch_player()
        vault_data = account.fetch_vault_info()
        vault_hashes = json_funcs.fetch_vault_hashes(vault_data)
        vault_items = InventoryManifest(vault_hashes)
        return vault_items.get_full_item_details(sort_by=sort)

    @staticmethod
    @tabulate_me
    def fetch_playtime(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        account.fetch_player()
        char_data = account.fetch_character_info()
        return json_funcs.fetch_play_time(char_data)

    @staticmethod
    @tabulate_me
    def fetch_last_time_played(guardian, platform):

        guardian, platform = PyGuardian.prechecks(guardian, platform)
        account = Requester(guardian, platform)
        account.fetch_player()
        char_data = account.fetch_character_info()
        return json_funcs.fetch_last_time_played(char_data)

    @staticmethod
    @log_me
    def prechecks(guardian, platform):

        get_manifest = GetManifest()
        check_manifest = CheckManifest()
        try:
            if not os.path.isdir(constants.DATA_DIR):
                print("Creating data directory")
                os.makedirs(constants.MANIFEST_DIR)
            if not os.path.isdir(constants.MANIFEST_DIR):
                print("Creating manifest directory")
                os.makedirs(constants.MANIFEST_DIR)
            if not os.path.isdir(constants.JSON_DIR):
                print("Creating JSON directory")
                os.makedirs(constants.JSON_DIR)
            if not os.listdir(str(Path.home()) + "/.pyguardian/DDB-Files"):
                print("Manifest files not available, requesting...")
                get_manifest(check_manifest())
        except OSError:
            raise CannotCreateStorageDirectories("Can't create directories!")

        uri = check_manifest()
        if uri is not None:
            get_manifest(uri)

        InputValidator.validate(guardian, platform)

        return GuardianProcessor.process(guardian, platform)
