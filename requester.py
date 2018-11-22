import requests
import asyncio
import logging
import json
import sys
import os


# Needed to prevent illegal cookie key messages
logging.disable()


class Requester:

    HEADERS = {"X-API-Key": os.environ["BUNGIE_API"]}
    PLATFORMS = {"xbox": "1", "playstation": "2", "pc": "4"}
    COMPONENTS = ["200", "102", "205"]

    def __init__(self, gamertag, platform):

        self.player_name = gamertag
        if not self.player_name:
            print("Must enter gamertag")
            sys.exit()
        # "#" must be replaced otherwise it breaks urls
        if "#" in self.player_name:
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

        r = self.fetch_url(self.search_url)

        if r["ErrorStatus"] == "SystemDisabled":
            print("API is down!")
            sys.exit()

        try:
            self.mem_id = r["Response"][0]["membershipId"]
        except IndexError:
            print("Can't find that player")
            sys.exit()

        print("Player found \u2713")

        data_url = self.root + self.mem_id + "/?components="

        urls = [data_url + comp for comp in self.COMPONENTS]

        self.chars_info = urls[0]
        self.vault_info = urls[1]
        self.char_equip = urls[2]

    def fetch_url(self, url):
        r = requests.get(url, headers=self.HEADERS)

        return r.json()
