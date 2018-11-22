from operator import itemgetter
import json


class InventoryManifest:

    def __init__(self, hash_lists):
        self.hashes = hash_lists

        with open("DDB-Files/DestinyInventoryItemDefinition.json", "r") as f:
            self.data = json.load(f)

        self.convert_hashes(self.hashes)

    def convert_hashes(self, hashes):

        self.final_hashes = []
        for character in hashes:
            character_list = []
            for hash_ in character:
                # Adding character attributes as section titles
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
                for k, v in self.data.items():
                    if hash_ == k:
                        # Not all manifest entries for player equipment
                        # have the same structure
                        if "itemTypeDisplayName" in v:
                            element = [v["displayProperties"]["name"],
                                       v["itemTypeDisplayName"],
                                       v["inventory"]["tierTypeName"]]
                            item_info.append(element)
                        else:
                            element = [v["displayProperties"]["name"],
                                       "", ""]
                            item_info.append(element)

        if sort_by == "name":
            item_info = sorted(item_info, key=itemgetter(0))
        elif sort_by == "type":
            item_info = sorted(item_info, key=itemgetter(1))
        elif sort_by == "tier":
            item_info = sorted(item_info, key=itemgetter(2))

        return item_info

    def get_item_names(self, whitespace=False):

        item_info = []
        for character in self.final_hashes:
            character_list = []
            for hash_ in character:
                if isinstance(hash_, list):
                    continue
                for k, v in self.data.items():
                    if hash_ == k:
                        if "itemTypeDisplayName" in v:
                            character_list.append(v["displayProperties"]["name"])
                        else:
                            character_list.append(v["displayProperties"]["name"])
            item_info.append(character_list)

        if whitespace:
            max_name_size = max([len(name[0]) for name in item_info])

            final_names = []
            for name in item_info:
                new_name = name[0] + (max_name_size - len(name[0])) * " "
                final_names.append([new_name])

            return final_names
        else:
            return item_info
