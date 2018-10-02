from aiohttp import ClientSession
import requests
import asyncio
import logging
import json
import sys
import os


# Needed to prevent illegal cookie key messages
logging.disable()


class PyGuardian:

    HEADERS = {"X-API-Key": os.environ["BUNGIE_API"]}
    PLATFORMS = {"xbox": "1", "playstation": "2", "pc": "4"}
    COMPONENTS = ["200", "102", "205"]

    def __init__(self, gamertag, platform):

        self.chars_info = None
        self.vault_info = None
        self.char_equip = None

        self.player_name = gamertag
        if not self.player_name:
            print("Must enter gamertag")
            sys.exit()

        try:
            self.platform = self.PLATFORMS[platform.lower()]
        except KeyError:
            print("No such platform")
            sys.exit()

        self.base = "https://www.bungie.net/Platform/Destiny2/"
        self.root = self.base + self.platform + "/Profile/"
        self.player_search = self.base + "SearchDestinyPlayer/" + self.platform + "/"

    async def fetch_eq(self):
        ''' Grab item hashes for all equipment '''
        if self.char_equip and self.chars_info:
            char_equip = self.char_equip
            char_info = self.chars_info
        else:
            await self.grab_player_data()
            char_equip = self.char_equip
            char_info = self.chars_info

        gens = {0: "Male", 1: "Female", 2: "Unknown"}
        races = {0: "Human", 1: "Awoken", 2: "Exo", 3: "Unknown"}
        classes = {0: "Titan", 1: "Hunter", 2: "Warlock", 3: "Unknown"}

        try:
            chars = list(char_info["Response"]["characters"]["data"].keys())
        except KeyError:
            print("No Destiny 2 information for this character")
            sys.exit()

        item_hashes = []
        for char in chars:
            items = char_equip["Response"]["characterEquipment"]["data"][char]["items"]
            # Slice to cut out banner, emblem and emote
            stats = char_info["Response"]["characters"]["data"][char]
            item_hashes.append([gens[stats["genderType"]].upper(),
                               races[stats["raceType"]].upper(),
                               classes[stats["classType"]].upper()])
            item_hashes += [item["itemHash"] for item in items[:12]]

        return item_hashes

    async def fetch_vault(self):
        ''' Get all contents in the player's vault '''
        if self.vault_info:
            vault_info = self.vault_info
        else:
            await self.grab_player_data()
            vault_info = self.vault_info

        if len(vault_info["Response"]["profileInventory"]) == 1:
            print("No vault information available")
            sys.exit()

        items = vault_info["Response"]["profileInventory"]["data"]["items"]

        item_hashes = [item["itemHash"] for item in items]

        return item_hashes

    async def fetch_play_time(self):
        ''' Return character playtime and total playtime '''
        if self.chars_info:
            char_info = self.chars_info
        else:
            await self.grab_player_data()
            char_info = self.chars_info

        try:
            self.chars = list(char_info["Response"]["characters"]["data"].keys())
        except KeyError:
            print("No Destiny 2 information for this character")
            sys.exit()

        char_mins = [char_info["Response"]["characters"]["data"][char]["minutesPlayedTotal"]
                                                                     for char in self.chars]

        char_mins = [int(element) for element in char_mins]

        hours, mins = divmod(sum(char_mins), 60)
        playtime_str = str(hours) + " hours and " + str(mins) + " minutes played"

        return char_mins, playtime_str

    async def fetch_char_info(self):
        ''' Get basic character information like power, mobility, etc '''
        if self.chars_info:
            char_info = self.chars_info
        else:
            await self.grab_player_data()
            char_info = self.chars_info

        char_info = self.chars_info

        gens = {0: "Male", 1: "Female", 2: "Unknown"}
        races = {0: "Human", 1: "Awoken", 2: "Exo", 3: "Unknown"}
        classes = {0: "Titan", 1: "Hunter", 2: "Warlock", 3: "Unknown"}

        try:
            chars = list(char_info["Response"]["characters"]["data"].keys())
        except KeyError:
            print("No Destiny 2 information for this character")
            sys.exit()

        char_stats = []
        for char in chars:
            stats = char_info["Response"]["characters"]["data"][char]
            char_attr = [gens[stats["genderType"]],
                         races[stats["raceType"]],
                         classes[stats["classType"]]]
            element = [" ".join(char_attr)]
            stats = char_info["Response"]["characters"]["data"][char]["stats"]
            element += [v for v in stats.values()]
            stats = char_info["Response"]["characters"]["data"][char]["levelProgression"]
            element.append(stats["level"])
            char_stats.append(element)

        return char_stats

    async def grab_player_data(self, player=None):
        ''' Use static methods to send asynchronous requests for player data '''
        if player is None:
            player = self.player_name

        r = requests.get(self.player_search + player,
                         headers=self.HEADERS).json()

        if r["ErrorStatus"] == "SystemDisabled":
            print("API is down!")
            sys.exit()

        print("Player found" + " \u2713")

        try:
            self.mem_id = r["Response"][0]["membershipId"]
        except IndexError:
            print("Can't find that player")
            sys.exit()

        data_url = self.root + self.mem_id + "/?components="

        urls = [data_url + comp for comp in self.COMPONENTS]

        print("Player data downloading...", end="")
        sys.stdout.flush()
        responses = await PyGuardian.gather(urls, self.HEADERS)

        self.chars_info = responses[0]
        self.vault_info = responses[1]
        self.char_equip = responses[2]
        print(" \u2713")

    async def write_data(self):
        data = await self.grab_player_data()

        with open("player_JSON/" + self.player_name + "_ch_eq.json", "w") as f,\
             open("player_JSON/" + self.player_name + "_va_in.json", "w") as f2,\
             open("player_JSON/" + self.player_name + "_ch_in.json", "w") as f3:
            json.dump(data[2], f, indent=4)
            json.dump(data[1], f2, indent=4)
            json.dump(data[0], f3, indent=4)

    @staticmethod
    async def fetch_url(url, headers, session):
        async with session.get(url, headers=headers) as response:
            return await response.json()

    @staticmethod
    async def gather(urls, headers):
        async with ClientSession() as session:
            tasks = [asyncio.ensure_future(PyGuardian.fetch_url(url, headers, session))
                                                                       for url in urls]

            responses =  await asyncio.gather(*tasks)

        return responses

