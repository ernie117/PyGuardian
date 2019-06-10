import os
from pathlib import Path


# Bungie API key stored as env variable
BUNGIE_API_KEY = os.environ["BUNGIE_API"]
HEADERS = {"X-API-Key": BUNGIE_API_KEY}

# URL-related constants
BASE = "https://www.bungie.net/Platform/Destiny2/"
COMPONENTS = ["200", "102", "205"]

# Directories needed for downloading and writing JSON
DATA_DIR = str(Path.home()) + "/.pyguardian"
JSON_DIR = DATA_DIR + "/DDB-Files"
MANIFEST_DIR = DATA_DIR + "/Destiny_Manifest"
MANIFEST_CHECK_FILE = DATA_DIR + "/Manifest-url-check.txt"
ZIP_FILE = MANIFEST_DIR + "/Destiny2Manifest.zip"
MANIFEST_URL_ROOT = "https://www.bungie.net"