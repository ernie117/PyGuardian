from aiohttp import ClientSession
import requests
import asyncio
import logging
import json
import sys
import os


logging.disable()


class PyGuardian:

    HEADERS = {"X-API-Key": os.environ["BUNGIE_API"]}
    root = "https://www.bungie.net/Platform/"
    component_schema = "/?components="
    platforms = {"xbox": "1", "playstation": "2", "pc": "4"}

    def __init__(self, gamertag, platform):
        self.player_name = gamertag

        if platform.lower() in self.platforms:
            platform = self.platforms[platform.lower()]

        self.profile = "Destiny2/" + platform + "/Profile/"
        self.player_search = "Destiny2/SearchDestinyPlayer/" + platform + "/"

    async def fetch_eq(self):
        ''' Grab item hashes for all equipment '''
        data = await self.grab_player_data()

        char_equip = data[3]

        chars = list(char_equip["Response"]["characterEquipment"]["data"].keys())

        item_hashes = []
        for char in chars:
            items = char_equip["Response"]["characterEquipment"]["data"][char]["items"]
            for item in items:
                item_hashes.append(item["itemHash"])

        return item_hashes

    async def fetch_vault(self):
        ''' Get all contents in the player's vault '''
        data = await self.grab_player_data()

        vault_info = data[2]

        items = vault_info["Response"]["profileInventory"]["data"]["items"]

        item_hashes = [item["itemHash"] for item in items]

        return item_hashes

    async def fetch_play_time(self):
        ''' Return character playtime and total playtime '''
        data = await self.grab_player_data()

        char_info = data[0]

        chars = list(char_info["Response"]["characters"]["data"].keys())

        char_mins = [char_info["Response"]["characters"]["data"][char]["minutesPlayedTotal"]
                                                                          for char in chars]

        char_mins = [int(element) for element in char_mins]

        hours, mins = divmod(sum(char_mins), 60)
        playtime_str = str(hours) + " hours and " + str(mins) + " minutes played"

        return char_mins, playtime_str

    async def fetch_char_info(self):
        ''' Get basic character information like power, mobility, etc '''
        data = await self.grab_player_data()

        char_info = data[0]

        chars = list(char_info["Response"]["characters"]["data"].keys())

        char_stats = []
        for char in chars:
            element = []
            stats = char_info["Response"]["characters"]["data"][char]["stats"]
            for v in stats.values():
                element.append(v)
            stats = char_info["Response"]["characters"]["data"][char]["levelProgression"]
            element.append(stats["level"])
            char_stats.append(element)

        return char_stats

    async def grab_player_data(self, player=None):
        ''' Use static methods to send asynchronous requests for player data '''
        if player is None:
            player = self.player_name

        r = requests.get(self.root
                       + self.player_search
                       + self.player_name,
                       headers=self.HEADERS)

        r = r.json()

        if r["ErrorStatus"] == "SystemDisabled":
            print("API is down!")
            sys.exit()

        self.mem_id = r["Response"][0]["membershipId"]

        char_info_url = (self.root
                       + self.profile
                       + self.mem_id
                       + self.component_schema
                       + "200")

        inventory_url = (self.root
                       + self.profile
                       + self.mem_id
                       + self.component_schema
                       + "201")

        vault_info_url = (self.root
                        + self.profile
                        + self.mem_id
                        + self.component_schema
                        + "102")

        char_equip_url = (self.root
                        + self.profile
                        + self.mem_id
                        + self.component_schema
                        + "205")

        urls = [char_info_url, inventory_url, vault_info_url, char_equip_url]

        responses = await PyGuardian.gather(urls, self.HEADERS)

        return responses

    async def write_data(self):
        data = await self.grab_player_data()

        with open("player_JSON/" + self.player_name + "_ch_eq.json", "w") as f,\
             open("player_JSON/" + self.player_name + "_va_in.json", "w") as f2,\
             open("player_JSON/" + self.player_name + "_ch_in.json", "w") as f3,\
             open("player_JSON/" + self.player_name + "_inv_in.json", "w") as f4:
            json.dump(data[3], f, indent=4)
            json.dump(data[2], f2, indent=4)
            json.dump(data[0], f3, indent=4)
            json.dump(data[1], f4, indent=4)

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

