from stat_data import StatData
from table_formatter import TableFormatter
import json

class InstanceData:

    dmg_types = {
            0: "Unknown",
            1: "Kinetic",
            2: "Arc",
            3: "Solar",
            4: "Void",
            5: "Raid"
    }

    def __init__(self, data):
        self.data = data

    def convert_hashes(self, hashes):
        final_hashes = []
        for item in hashes:
            if (item & (1 << (32 - 1))) != 0:
                item = item - (1 << 32)
                final_hashes.append(str(item))
            else:
                final_hashes.append(str(item))

        return final_hashes

    def get_stats(self):

        chars = len(self.data) // 3

        damages = []
        final_data = []
        titles = []
        for entry in self.data:
            element = []
            stat_hashes = []
            stat_values = []
            element.append(self.dmg_types[entry["Response"]["instance"]["data"]["damageType"]])
            element.append(entry["Response"]["instance"]["data"]["primaryStat"]["value"])
            stats = entry["Response"]["stats"]["data"]["stats"]
            stat_keys = list(entry["Response"]["stats"]["data"]["stats"].keys())
            for key in stat_keys:
                stat_hashes.append(stats[key]["statHash"])
                stat_values.append(stats[key]["value"])

            final_hashes = self.convert_hashes(stat_hashes)

            title = []
            stat_data, title = StatData(final_hashes, stat_values).get_stat_data()
            element += stat_data
            final_title = TableFormatter(title).format()
            titles.append(final_title)
            final_data.append(element)

        return titles, final_data

    def get_perk_hashes(self):
        pass

