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

    dates = []
    sessions = []
    data = JSONMiner(root_str, character_data)
    for char in characters:
        date = dateutil.parser.parse(data[char]["dateLastPlayed"])
        date = date.strftime("%H:%M:%S -- %a %d/%m")
        dates.append(date)
        session = int(data[char]["minutesPlayedThisSession"])
        hours, minutes = divmod(session, 60)
        session = str(hours) + " hours and " + str(minutes) + " minutes"
        sessions.append(session)

    time_data = [date + " for " + session for date, session in zip(dates, sessions)]

    return time_data


def fetch_play_time(character_data):

    root_str = "Response.characters.data."

    try:
        characters = list(JSONMiner(root_str, character_data).keys())
    except KeyError:
        print("No data for this character")
        sys.exit()

    char_mins = [int(JSONMiner(f"{root_str}{char}.minutesPlayedTotal", character_data))
                                                                for char in characters]

    hours, mins = divmod(sum(char_mins), 60)
    playtime_str = (str(hours)
                   + " hours and "
                   + str(mins)
                   + " minutes played")

    return char_mins, playtime_str


def fetch_vault_hashes(vault_info):

    root_str = "Response.profileInventory.data.items"

    # Default privacy settings block vault access
    if len(vault_info["Response"]["profileInventory"]) == 1:
        print("No vault information available")
        sys.exit()

    items = JSONMiner(root_str, vault_info)

    item_hashes = [item["itemHash"] for item in items]

    return [item_hashes]



