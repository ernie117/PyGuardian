import requests
import sys
import os


class Requester:
    HEADERS = {"X-API-Key": os.environ["BUNGIE_API"]}
    PLATFORMS = {"xbox": "1", "playstation": "2", "pc": "4"}
    COMPONENTS = ["200", "102", "205"]

    def __init__(self, gamertag, platform):

        self.player_name = gamertag

        self.character_info_url = None
        self.vault_info_url = None
        self.character_equip_url = None
        self.mem_id = None

        # "#" is present in BattleID's on pc but they must be replaced
        self.player_name = self.player_name.replace("#", "%23")

        try:
            self.platform = self.PLATFORMS[platform.lower()]
        except KeyError:
            print("No such platform")
            sys.exit()

        self.base = "https://www.bungie.net/Platform/Destiny2/"
        self.root = self.base + self.platform + "/Profile/"
        self.player_search = self.base + "SearchDestinyPlayer/" + self.platform + "/"

        self.search_url = self.player_search + self.player_name

    def fetch_player(self):

        r = requests.get(self.search_url, headers=self.HEADERS).json()

        if r["ErrorStatus"] == "SystemDisabled":
            print("API is down!")
            sys.exit()

        try:
            self.mem_id = r["Response"][0]["membershipId"]
        except IndexError:
            print("Can't find that player")
            sys.exit()

        print("Player found \u2713")

        urls = [self.root + self.mem_id + "/?components=" + comp
                for comp in self.COMPONENTS]

        self.character_info_url = urls[0]
        self.vault_info_url = urls[1]
        self.character_equip_url = urls[2]

    def fetch_character_info(self):
        r = requests.get(self.character_info_url, headers=self.HEADERS)

        return r.json()

    def fetch_vault_info(self):
        r = requests.get(self.vault_info_url, headers=self.HEADERS)

        return r.json()

    def fetch_character_equip_info(self):
        r = requests.get(self.character_equip_url, headers=self.HEADERS)

        return r.json()
