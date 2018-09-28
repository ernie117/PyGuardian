import json


class InventoryManifest:

    def __init__(self, item_hashes):
        self.hashes = item_hashes

        with open("DDB-Files/DestinyInventoryItemDefinition.json", "r") as f:
            self.data = json.load(f)


    def get_items(self):

        item_info = []
        final_hashes = []
        for item in self.hashes:
            if isinstance(item, list):
                final_hashes.append(item)
                continue
            elif (item & (1 << (32 - 1))) != 0:
                item = item - (1 << 32)
                final_hashes.append(str(item))
            else:
                final_hashes.append(str(item))

        for hash_ in final_hashes:
            if isinstance(hash_, list):
                item_info.append(hash_)
                continue
            for k, v in self.data.items():
                if hash_ == k:
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
