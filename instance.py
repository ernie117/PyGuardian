import json
from pprint import pprint

class InstanceData:

    dmg_types = {0: "Unknown", 1: "Kinetic", 2: "Arc",
                 3: "Solar", 4: "Void", 5: "Raid"}

    def __init__(self, data):
        self.data = data

    def get_stats(self):
        with open("DDB-Files/DestinySandboxPerkDefinition.json", "r") as f:
            manifest = json.load(f)

        chars = len(self.data) // 3

        for entry in self.data:
            print(entry["Response"]["instance"]["data"]["primaryStat"]["value"])

    def get_perks(self):
        pass

