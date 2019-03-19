""" This class holds a collection of methods that offload all
the heavy lifting of requesting and processing to other modules,
for easy command line use with destiny_cli and interactive terminal
use """
from hashes import InventoryManifest
from requester import Requester
from tabulate import tabulate
from pathlib import Path
import get_manifest
import json_funcs
import os


class PyGuardian:

    @staticmethod
    def prechecks():
        if not os.path.isdir(str(Path.home()) + "/Documents/python/PyGuardian/DDB-Files"):
            print("Manifest files not available, requesting...")
            get_manifest.main()

    @staticmethod
    def fetch_stats(guardian, platform):

        PyGuardian.prechecks()
        account = Requester(guardian, platform)
        account.fetch_player()
        response = account.fetch_character_info()
        data = json_funcs.fetch_char_info(response)
        table = tabulate(data, headers="keys", tablefmt="fancy_grid")

        return table

    @staticmethod
    def fetch_eq(guardian, platform):

        PyGuardian.prechecks()
        account = Requester(guardian, platform)
        account.fetch_player()
        char_data = account.fetch_character_info()
        equip_data = account.fetch_character_equip_info()
        weapon_hashes = json_funcs.fetch_eq_hashes(equip_data, char_data)
        weapon_data = InventoryManifest(weapon_hashes)
        weapon_data = weapon_data.get_full_item_details()
        table = tabulate(weapon_data, tablefmt="fancy_grid")

        return table

    @staticmethod
    def fetch_vault(guardian, platform, sort=None):

        PyGuardian.prechecks()
        account = Requester(guardian, platform)
        account.fetch_player()
        vault_data = account.fetch_vault_info()
        vault_hashes = json_funcs.fetch_vault_hashes(vault_data)
        vault_items = InventoryManifest(vault_hashes)
        vault_items = vault_items.get_full_item_details(sort_by=sort)
        table = tabulate(vault_items, tablefmt="fancy_grid")

        return table

    @staticmethod
    def fetch_playtime(guardian, platform):

        PyGuardian.prechecks()
        account = Requester(guardian, platform)
        account.fetch_player()
        char_data = account.fetch_character_info()
        char_dicts = json_funcs.fetch_play_time(char_data)
        table = tabulate(char_dicts, headers="keys", tablefmt="fancy_grid")

        return table

    @staticmethod
    def fetch_last_time_played(guardian, platform):

        PyGuardian.prechecks()
        account = Requester(guardian, platform)
        account.fetch_player()
        char_data = account.fetch_character_info()
        playtimes = json_funcs.fetch_last_time_played(char_data)
        table = tabulate(playtimes, headers="keys", tablefmt="fancy_grid")

        return table
