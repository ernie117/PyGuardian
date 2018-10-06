import json


class InventoryManifest:

    def __init__(self, item_hashes):
        self.hashes = item_hashes

        with open("DDB-Files/DestinyInventoryItemDefinition.json", "r") as f:
            self.data = json.load(f)

        self.convert_hashes(self.hashes)

    def convert_hashes(self, hashes):

        self.final_hashes = []
        for item in hashes:
            # Adding character attributes as section titles
            if isinstance(item, list):
                self.final_hashes.append(item)
            # Converting hash if it needs to be
            elif (item & (1 << (32 - 1))) != 0:
                item = item - (1 << 32)
                self.final_hashes.append(str(item))
            else:
                self.final_hashes.append(str(item))

    def get_full_items(self):

        item_info = []
        for hash_ in self.final_hashes:
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

        return item_info

    def get_partial_items(self):

        item_info = []
        for hash_ in self.final_hashes:
            if isinstance(hash_, list):
                continue
            for k, v in self.data.items():
                if hash_ == k:
                    if "itemTypeDisplayName" in v:
                        element = [v["displayProperties"]["name"].upper()]
                        item_info.append(element)
                    else:
                        element = [v["displayProperties"]["name"].upper()]
                        item_info.append(element)

        max_name_size = max([len(name[0]) for name in item_info])

        final_names = []
        for name in item_info:
            new_name = name[0] + (max_name_size - len(name[0])) * " "
            final_names.append([new_name])

        return final_names
