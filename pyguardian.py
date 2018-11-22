''' This class holds a collection of methods that offload all
the heavy lifting of requesting and processing to other modules,
for easy command line use with destiny_cli and interactive terminal
use '''
from hashes import InventoryManifest
from requester import Requester
from tabulate import tabulate
import json_funcs


class PyGuardian:

    @staticmethod
    def fetch_stats(guardian, platform):

        account = Requester(guardian, platform)
        account.fetch_player()
        response = account.fetch_url(account.chars_info)
        data = json_funcs.fetch_char_info(response)
        table = tabulate(data, headers="keys", tablefmt="fancy_grid")

        return table

    @staticmethod
    def fetch_eq(guardian, platform):

        account = Requester(guardian, platform)
        account.fetch_player()
        char_data = account.fetch_url(account.chars_info)
        equip_data = account.fetch_url(account.char_equip)
        weapon_hashes = json_funcs.fetch_eq_hashes(equip_data, char_data)
        weapon_data = InventoryManifest(weapon_hashes)
        weapon_data = weapon_data.get_full_item_details()
        table = tabulate(weapon_data, tablefmt="fancy_grid")

        return table

    @staticmethod
    def fetch_vault(guardian, platform, sort_by=None):

        account = Requester(guardian, platform)
        account.fetch_player()
        vault_data = account.fetch_url(account.vault_info)
        vault_hashes = json_funcs.fetch_vault_hashes(vault_data)
        vault_items = InventoryManifest(vault_hashes)

        if sort_by == "name":
            vault_items = vault_items.get_full_item_details(sort_by="name")
        elif sort_by == "type":
            vault_items = vault_items.get_full_item_details(sort_by="type")
        elif sort_by == "tier":
            vault_items = vault_items.get_full_item_details(sort_by="tier")
        else:
            vault_items = vault_items.get_full_item_details()

        table = tabulate(vault_items, tablefmt="fancy_grid")

        return table

    @staticmethod
    def fetch_playtime(guardian, platform):
        pass

    @staticmethod
    def fetch_last_played(guardian, platform):
        pass
