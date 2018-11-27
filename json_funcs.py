from hashes import InventoryManifest
import dateutil.parser
import asyncio
import sys


GENS = {0: "Male", 1: "Female", 2: "Unknown"}
RACES = {0: "Human", 1: "Awoken", 2: "Exo", 3: "Unknown"}
CLASSES = {0: "Titan", 1: "Hunter", 2: "Warlock", 3: "Unknown"}


def JSONMiner(string, data):
    queries = string.split(".")
    query = queries[0]
    value = None
    try:
        string = '.'.join(queries[1:])
    except IndexError:
        return data

    if isinstance(data, dict):
        value = data[query]
        data = data[query]
    elif isinstance(data, list):
        value = data[query]
        data = data[query]

    if string:
        return JSONMiner(string, data)

    return value


def fetch_eq_hashes(equipment_data, character_data):

    root_str1 = "Response.characters.data."
    root_str2 = "Response.characterEquipment.data."

    try:
        characters = list(JSONMiner(root_str1, character_data).keys())
    except KeyError:
        print("No Destiny 2 information for this character")
        sys.exit()

    item_hashes = []
    for char in characters:
        element = []
        title = JSONMiner(f"{root_str1}{char}", character_data)
        char_title = ([GENS[title["genderType"]].upper(),
                       RACES[title["raceType"]].upper(),
                       CLASSES[title["classType"]].upper()])
        element.append(char_title)
        items = JSONMiner(f"{root_str2}{char}.items", equipment_data)[:11]
        element.extend([item["itemHash"] for item in items])
        item_hashes.append(element)

    return item_hashes


def fetch_char_info(character_data):

    root_str = "Response.characters.data."

    char_dictionaries = []
    char_dict = {
            "Character":  None,
            "Power":      None,
            "Mobility":   None,
            "Resilience": None,
            "Recovery":   None,
            "Level":      None
        }

    try:
        characters = list(JSONMiner(root_str, character_data).keys())
    except KeyError:
        print("No data for this character")
        sys.exit()

    query_strings = [root_str + char for char in characters]

    for char in query_strings:
        stats_list = []
        stats = JSONMiner(char, character_data)
        stats_list.append(" ".join([GENS[stats["genderType"]],
                                    RACES[stats["raceType"]],
                                    CLASSES[stats["classType"]]]))
        stats = JSONMiner(f"{char}.stats", character_data)
        stats_list.extend([v for v in stats.values()])
        stats_list.append(JSONMiner(f"{char}.levelProgression.level", character_data))
        char_dict = {k: stat for k, stat in zip(char_dict, stats_list)}
        char_dictionaries.append(char_dict)

    return char_dictionaries


def fetch_last_time_played(character_data):

    root_str = "Response.characters.data."

    try:
        characters = list(JSONMiner(root_str, character_data).keys())
    except KeyError:
        print("No data for this character")
        sys.exit()

    char_dict = {
            "Character": None,
            "Datetime":  None,
            "Session":   None,
        }

    char_dicts = []
    data = JSONMiner(root_str, character_data)
    for char in characters:
        char_str = []
        char_info = data[char]
        char_title = (" ".join([GENS[char_info["genderType"]],
                                RACES[char_info["raceType"]],
                                CLASSES[char_info["classType"]]]))
        char_str.append(char_title)
        date = dateutil.parser.parse(data[char]["dateLastPlayed"])
        date = date.strftime("%H:%M:%S -- %a %d/%m")
        char_str.append(date)
        session = int(data[char]["minutesPlayedThisSession"])
        hours, minutes = divmod(session, 60)
        session = str(hours) + " hours and " + str(minutes) + " minutes"
        char_str.append(session)
        char_dicts.append({k: info for k, info in zip(char_dict, char_str)})

    return char_dicts


def fetch_play_time(character_data):

    root_str = "Response.characters.data."

    try:
        characters = list(JSONMiner(root_str, character_data).keys())
    except KeyError:
        print("No data for this character")
        sys.exit()

    char_mins = [int(JSONMiner(f"{root_str}{char}.minutesPlayedTotal", character_data))
                                                                for char in characters]

    readable_times = (divmod(time, 60) for time in char_mins)
    readable_times = [f"{time[0]}h {time[1]}m" for time in readable_times]
    total_hours, total_mins = divmod(sum(char_mins), 60)
    playtime_str = str(total_hours) + "h " + str(total_mins) + "m"

    char_titles = []
    for char in characters:
        char_data = JSONMiner(f"{root_str}{char}", character_data)
        char_titles.append(" ".join([GENS[char_data["genderType"]],
                                     RACES[char_data["raceType"]],
                                     CLASSES[char_data["classType"]]]))

    char_dicts = []
    for char, time in zip(char_titles, readable_times):
        character = {}
        character["Character"] = char
        character["Time"] = time
        char_dicts.append(character)

    char_dicts.append({"Character": "TOTAL",
                       "Time": playtime_str})

    return char_dicts


def fetch_vault_hashes(vault_info):

    root_str = "Response.profileInventory.data.items"

    try:
        items = JSONMiner(root_str, vault_info)
        item_hashes = [item["itemHash"] for item in items]

        return [item_hashes]

    except KeyError:
        print("Vault access blocked")
        sys.exit()




