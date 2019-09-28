import os
from pathlib import Path


# Bungie API key stored as env variable
BUNGIE_API_KEY = os.environ["BUNGIE_API"]
HEADERS = {"X-API-Key": BUNGIE_API_KEY}

# URL-related constants
BASE = "https://www.bungie.net/Platform/Destiny2/"
COMPONENTS = ["200", "102", "205"]
MANIFEST_URL = BASE + "Manifest/"

# Directories needed for downloading and writing JSON
DATA_DIR = str(Path.home()) + "/.pyguardian"
JSON_DIR = DATA_DIR + "/DDB-Files"
CHARACTER_JSON_DIR = DATA_DIR + "/character-json"
MANIFEST_DIR = DATA_DIR + "/Destiny_Manifest"
MANIFEST_CHECK_FILE = DATA_DIR + "/Manifest-url-check.txt"
ZIP_FILE = MANIFEST_DIR + "/Destiny2Manifest.zip"
MANIFEST_URL_ROOT = "https://www.bungie.net"

# InventoryItemDefinition file path
INVENTORY_JSON_FILE = str(Path.home()) + "/.pyguardian/DDB-Files/DestinyInventoryItemDefinition.json"

# Default logging file path
DEFAULT_LOGGING_PATH = str(Path.home()) + "/.pyguardian/" + "default-log-file"

# Dictionary for initialising Guardian class
GUARDIAN_INIT_DICT = {
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
