import os

TEST_DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + "/dummy_inventoryItemDefinition.json"
TEST_CHAR_DATA = os.path.dirname(os.path.realpath(__file__)) + "/dummy_character_data.json"
TEST_EQUIP_DATA = os.path.dirname(os.path.realpath(__file__)) + "/dummy_equip_data.json"
TEST_VAULT_DATA = os.path.dirname(os.path.realpath(__file__)) + "/dummy_vault_data.json"

TEST_EQ_HASHES = [
    [
        ["MALE", "EXO", "WARLOCK"],
        2712244741, 1887808042,
        1201830623, 381563628,
        3830828709, 3192591867,
        4178158375, 1549308050,
        813936739, 1363029408,
        2844014413
    ]
]

EXPECTED_EQ_HASHES_CHAR_ONE = [
    ["MALE", "EXO", "WARLOCK"],
    2712244741, 1887808042,
    1201830623, 381563628,
    3830828709, 3192591867,
    4178158375, 1549308050,
    813936739, 1363029408,
    2844014413, 3887892656
]

EXPECTED_EQ_HASHES_CHAR_TWO = [
    ["MALE", "HUMAN", "TITAN"],
    1457394911, 1678957659,
    1877183765, 1070180272,
    809007411, 201644247,
    2362809459, 2329963686,
    3717471208, 2351197433,
    682682138, 2958378809
]

EXPECTED_VAULT_HASHES = [
    4285666432, 2014411539, 4101386442,
    1177810185, 2109561326, 950899352
]

VAULT_HASHES = [
    4285666432, 2014411539, 4101386442,
    1177810185, 2109561326, 950899352
]

TEST_ITEM_RESULT = ["Bygones", "Pulse Rifle", "Legendary"]
EXPECTED_CHAR_INFO_KEYS = ["Character", "Power", "Mobility",
                           "Resilience", "Recovery", "Level"]
EXPECTED_LAST_PLAYED_KEYS = ["Character", "Datetime", "Session"]
EXPECTED_PLAY_TIME_KEYS = ["Character", "Time"]
FETCH_STATS_MOCK_RESP = "│ Character │ Power │ Mobility │  Resilience │ Recovery │  Level │"
FETCH_EQ_MOCK_RESP = "│ MALE │ EXO │ WARLOCK │"
