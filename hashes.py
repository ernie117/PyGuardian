from operator import itemgetter
import json


class InventoryManifest:

    def __init__(self, hash_lists):
        self.hashes = hash_lists
        self.final_hashes = []

        with open("/home/user-admin/Documents/python/PyGuardian/DDB-Files/DestinyInventoryItemDefinition.json", "r") as f:
            self.data = json.load(f)

        self.convert_hashes(self.hashes)

    def convert_hashes(self, hashes):

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

    def get_full_item_details(self, sort_by=None):

        item_info = []
        for character in self.final_hashes:
            for hash_ in character:
                if isinstance(hash_, list):
                    item_info.append(hash_)
                    continue
                if hash_ in self.data:
                    # Not all item entries have the same JSON structure
                    try:
                        element = [self.data[hash_]["displayProperties"]["name"],
                                   self.data[hash_]["itemTypeDisplayName"],
                                   self.data[hash_]["inventory"]["tierTypeName"]]
                        item_info.append(element)
                    except KeyError:
                        element = [self.data[hash_]["displayProperties"]["name"],
                                   "", ""]
                        item_info.append(element)

        # Sorting alphabetically by item name, type of item
        # or item rarity e.g. legendary, exotic
        if sort_by == "name":
            item_info = sorted(item_info, key=itemgetter(0))
        elif sort_by == "type":
            item_info = sorted(item_info, key=itemgetter(1))
        elif sort_by == "tier":
            item_info = sorted(item_info, key=itemgetter(2))

        return item_info

    def get_item_names(self):

        item_info = []
        for character in self.final_hashes:
            character_list = []
            for hash_ in character:
                if isinstance(hash_, list):
                    continue
                if hash_ in self.data:
                    character_list.append(v["displayProperties"]["name"])
            item_info.append(character_list)

        return item_info
