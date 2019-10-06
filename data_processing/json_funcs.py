"""
A collection of pure functions used for parsing JSON returned
from the Bungie API, extracting specific values and arranging
them into data structures suitable for tabulate tables or
marshalling into a Guardian class
"""
from typing import List, Union, Dict, AnyStr

import dateutil.parser

from pyguardian.validation.pyguardian_exceptions import PlayerNotFoundException, VaultAccessBlockedException, \
    NoPlayerEquipmentException, APIException
from pyguardian.utils.pyguardian_decorators import log_me
from pyguardian.main.guardian import Guardian
from pyguardian.data_processing.hashes import InventoryManifest


GENS = {0: "Male", 1: "Female", 2: "Unknown"}
RACES = {0: "Human", 1: "Awoken", 2: "Exo", 3: "Unknown"}
CLASSES = {0: "Titan", 1: "Hunter", 2: "Warlock", 3: "Unknown"}


@log_me
def fetch_eq_hashes(equipment_data: dict, character_data: dict) -> List[list]:
    check_response(equipment_data, character_data)
    root_str1 = "Response.characters.data."
    root_str2 = "Response.characterEquipment.data."

    characters = get_character_ids(root_str1, character_data)

    item_hashes = []
    for char in characters:
        element = []
        title = json_miner(f"{root_str1}{char}", character_data)
        # Adding a title row that describes the character
        # to distinguish between multiple characters
        char_title = [string.upper() for string in get_character_titles(title)]
        char_title.append("SCREENSHOT - www.bungie.net +")
        element.append(char_title)
        try:
            items = json_miner(f"{root_str2}{char}.items", equipment_data)
        except KeyError:
            raise NoPlayerEquipmentException(f"No equipment data found for {char}")
        element.extend([item["itemHash"] for item in items])
        item_hashes.append(element)

    return item_hashes


@log_me
def fetch_character_eq_details(equipment_data: dict, character_data: dict) -> List[list]:
    check_response(equipment_data, character_data)
    root_str1 = "Response.characters.data."
    root_str2 = "Response.characterEquipment.data."

    characters = get_character_ids(root_str1, character_data)

    character_items_lists = []
    for char in characters:
        element = []
        item_hashes = []
        title = json_miner(f"{root_str1}{char}", character_data)
        char_title = [string.upper() for string in get_character_titles(title)]
        element.append(char_title)
        try:
            items = json_miner(f"{root_str2}{char}.items", equipment_data)
        except KeyError:
            raise NoPlayerEquipmentException(f"No equipment data found for {char}")
        element.extend([item["itemHash"] for item in items])
        item_hashes.append(element)
        data = InventoryManifest(item_hashes)
        character_items_lists.append(data.get_full_item_details())

    return character_items_lists


@log_me
def fetch_char_info(character_data: dict) -> List[dict]:
    check_response(character_data)
    root_str = "Response.characters.data."

    char_dictionaries = []
    char_dict = {
        "Character": None,
        "Power": None,
        "Mobility": None,
        "Resilience": None,
        "Recovery": None,
        "Level": None
    }

    characters = get_character_ids(root_str, character_data)
    query_strings = [root_str + char for char in characters]

    for char in query_strings:
        stats_list = []
        stats = json_miner(char, character_data)
        stats_list.append(" ".join(get_character_titles(stats)))
        stats = json_miner(f"{char}.stats", character_data)
        stats_list.extend([v for v in stats.values()])
        stats_list.append(json_miner(f"{char}.levelProgression.level", character_data))
        char_dict = {k: stat for k, stat in zip(char_dict, stats_list)}
        char_dictionaries.append(char_dict)

    return char_dictionaries


@log_me
def fetch_extended_char_info(character_data: dict, equipment_data: List[list], guardian: str) -> List[dict]:
    check_response(character_data)
    root_str = "Response.characters.data."

    extended_char_dict = {
        "_gamertag": None,
        "_character_id": None,
        "_membership_id": None,
        "_membership_type": None,
        "_date_last_played": None,
        "_total_mins_played": None,
        "_gender": None,
        "_race": None,
        "_class": None,
        "_subclass": None,
        "_level": None,
        "_light": None,
        "_mobility": None,
        "_resilience": None,
        "_recovery": None,
        "_emblem_path": None,
    }

    # Subclass is in equipment data rather than character data
    # ¯\_(ツ)_/¯
    subclasses = []
    for char in equipment_data:
        for item in char:
            for element in item:
                if "subclass" in element.lower():
                    subclasses.append(item[0])

    characters = get_character_ids(root_str, character_data)
    query_strings = [root_str + char for char in characters]

    char_dictionaries = []
    for i, char in enumerate(query_strings):
        stats_list = [guardian]
        stats = json_miner(char, character_data)
        emblem_path = stats["emblemBackgroundPath"]
        stats_list.extend([stats["characterId"],
                           stats["membershipId"],
                           stats["membershipType"],
                           stats["dateLastPlayed"],
                           stats["minutesPlayedTotal"]])
        gender, race, class_ = get_character_titles(stats)
        stats_list.extend([gender, race, class_, subclasses[i]])
        stats_list.append(json_miner(f"{char}.levelProgression.level", character_data))
        stats = json_miner(f"{char}.stats", character_data)
        stats_list.extend([v for v in stats.values()])
        stats_list.append(emblem_path)
        char_dict = {k: stat for k, stat in zip(extended_char_dict, stats_list)}
        char_dictionaries.append(char_dict)

    return char_dictionaries


@log_me
def fetch_last_time_played(character_data: dict) -> List[dict]:
    check_response(character_data)
    root_str = "Response.characters.data."

    characters = get_character_ids(root_str, character_data)

    char_dict = {
        "Character": None,
        "Datetime": None,
        "Session": None,
    }

    char_dicts = []
    data = json_miner(root_str, character_data)
    for char in characters:
        char_str = []
        char_info = data[char]
        char_title = (" ".join(get_character_titles(char_info)))
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


@log_me
def fetch_play_time(character_data: dict) -> List[dict]:
    check_response(character_data)
    root_str = "Response.characters.data."

    characters = get_character_ids(root_str, character_data)

    char_mins = [int(json_miner(f"{root_str}{char}.minutesPlayedTotal", character_data))
                 for char in characters]

    readable_times = (divmod(time, 60) for time in char_mins)
    readable_times = [f"{time[0]}h {time[1]}m" for time in readable_times]
    total_hours, total_mins = divmod(sum(char_mins), 60)
    playtime_str = f"{total_hours}h {total_mins}m"

    char_titles = []
    for char in characters:
        char_data = json_miner(f"{root_str}{char}", character_data)
        char_titles.append(" ".join(get_character_titles(char_data)))

    char_dicts = []
    for char, time in zip(char_titles, readable_times):
        character = dict()
        character["Character"] = char
        character["Time"] = time
        char_dicts.append(character)

    char_dicts.append({"Character": "TOTAL",
                       "Time": playtime_str})

    return char_dicts


@log_me
def fetch_vault_hashes(vault_info: dict) -> List[list]:
    check_response(vault_info)
    root_str = "Response.profileInventory.data.items"

    try:
        items = json_miner(root_str, vault_info)
        item_hashes = [item["itemHash"] for item in items]

        return [item_hashes]

    except KeyError:
        raise VaultAccessBlockedException("Vault access blocked for this character")


@log_me
def fetch_kd(stats_json: dict, char_data: dict) -> List[dict]:
    check_response(stats_json, char_data)
    root_str = "Response.characters.data."
    root_str_2 = "Response.characters"
    root_str_3 = "results.allPvP.allTime.killsDeathsRatio.basic.displayValue"
    root_str_4 = "Response.mergedAllCharacters.results.allPvP.allTime.killsDeathsRatio.basic.displayValue"

    characters = get_character_ids(root_str, char_data)

    char_titles = dict()
    for character in characters:
        char_obj = json_miner(f"{root_str}{character}", char_data)
        char_titles[char_obj["characterId"]] = " ".join(get_character_titles(char_obj))

    char_objects = json_miner(root_str_2, stats_json)
    character_kds = []
    for obj in char_objects:
        for char in char_titles:
            if obj["characterId"] in char:
                character = dict()
                character["Character"] = char_titles[char]
                character["Kill/Death Ratio"] = json_miner(root_str_3, obj)
                character_kds.append(character)

    character_kds.append({"Character": "Overall",
                          "Kill/Death Ratio": json_miner(root_str_4, stats_json)})

    return character_kds


@log_me
def get_data_guardian_objects(char_data: List[dict], equip_data: List[list]) -> List[Guardian]:
    eq_dict = {
        "_primary": None,
        "_secondary": None,
        "_heavy": None,
        "_helmet": None,
        "_gauntlets": None,
        "_chest": None,
        "_greaves": None,
        "_class_item": None,
        "_ghost": None,
        "_sparrow": None,
        "_ship": None
    }

    characters = []
    for character in equip_data:
        # equipment list contains unwanted character description
        filtered = [hash_ for hash_ in character if "MALE" not in hash_ and "FEMALE" not in hash_]
        characters.append({k: v for k, v in zip(eq_dict, filtered)})

    return [Guardian({**char[0], **char[1]}) for char in list(zip(char_data, characters))]


# Common utility functions


def json_miner(string: str, data: Union[Dict, List]) -> Union[Dict, List[Dict], AnyStr]:
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
        value = data[int(query)]
        data = data[int(query)]

    if string:
        return json_miner(string, data)

    return value


def get_character_ids(root_str: str, char_data: dict):
    try:
        return list(json_miner(root_str, char_data).keys())
    except KeyError:
        raise PlayerNotFoundException("No Destiny 2 information for this character")


def get_character_titles(char_object: dict):
    return [GENS[char_object["genderType"]], RACES[char_object["raceType"]], CLASSES[char_object["classType"]]]


def check_response(*args: Union[List[dict], dict]):
    for response in args:
        if "ErrorStatus" in response.keys() and response["ErrorStatus"] == "UnhandledException":
            raise APIException(f"API is down: {response['Message']}")
