import json


class StatData:

    def __init__(self, stat_hashes, stat_values):
        self.hashes = stat_hashes
        self.values = stat_values

        with open("DDB-Files/DestinyStatDefinition.json", "r") as f:
            self.data = json.load(f)

        self.get_stat_data()

    def get_stat_data(self):

        stat_data = []
        stat_titles = []
        for hash_, value in zip(self.hashes, self.values):
            if hash_ in self.data:
                stat_titles.append(self.data[hash_]["displayProperties"]["name"])
                stat_data.append(value)

        return stat_data, stat_titles
