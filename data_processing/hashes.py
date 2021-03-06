import json
from operator import itemgetter

from pyguardian.utils.constants import INVENTORY_JSON_FILE
from pyguardian.utils.pyguardian_decorators import log_me


class InventoryManifest:

    def __init__(self, hash_lists, inventory_file=INVENTORY_JSON_FILE):
        self.hashes = hash_lists
        self.final_hashes = []

        with open(inventory_file, "r") as f:
            self.data = json.load(f)

        self._convert_hashes(self.hashes)

    @log_me
    def _convert_hashes(self, hashes):

        for character in hashes:
            character_list = []
            for hash_ in character:
                # Adding character attributes as section titles
                # e.g. ['Male', 'Exo', 'Titan']
                if isinstance(hash_, list):
                    character_list.append(hash_)
                # Converting hash if it needs to be
                elif (hash_ & (1 << (32 - 1))) != 0:
                    hash_ = hash_ - (1 << 32)
                    character_list.append(str(hash_))
                else:
                    character_list.append(str(hash_))
            self.final_hashes.append(character_list)

    @log_me
    def get_full_item_details(self, sort_by=None):

        item_info = []
        for character in self.final_hashes:
            for hash_ in character:
                if isinstance(hash_, list):
                    item_info.append(hash_)
                    continue
                # Not all item entries have the same JSON structure
                try:
                    item_info.append(
                        [self.data[hash_]["displayProperties"]["name"],
                         self.data[hash_]["itemTypeDisplayName"],
                         self.data[hash_]["inventory"]["tierTypeName"]]
                    )
                except KeyError:
                    element = [self.data[hash_]["displayProperties"]["name"],
                               "", ""]
                    item_info.append(element)

        # Sorting alphabetically by item name, type of item
        # or item rarity -- only for vault items
        if sort_by == "name":
            item_info = sorted(item_info, key=itemgetter(0))
        elif sort_by == "type":
            item_info = sorted(item_info, key=itemgetter(1))
        elif sort_by == "tier":
            item_info = sorted(item_info, key=itemgetter(2))

        return item_info

