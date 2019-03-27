from time import sleep
from pathlib import Path
import requests
import shutil
import sqlite3
import json
import zipfile
import sys
import os


HEADERS = {"X-API-Key": os.environ["BUNGIE_API"]}
WORKING_DIR = str(Path.home()) + "/Documents/python/PyGuardian"
DATA_DIR = str(Path.home()) + "/.pyguardian"
MANIFEST_DIR = DATA_DIR + "/Destiny_Manifest"
JSON_DIR = DATA_DIR + "/DDB-Files"
MANIFEST_CHECK_FILE = DATA_DIR + "/Manifest-url-check.txt"
ZIP_FILE = MANIFEST_DIR + "/Destiny2Manifest.zip"
MANIFEST_URL_ROOT = "https://www.bungie.net"


def main(skip_check=False):

    check_dirs()
    manifest_uri = get_manifest_url()
    if skip_check:
        get_manifest(MANIFEST_URL_ROOT + manifest_uri)
    else:
        if check_manifest_url(manifest_uri):
            get_manifest(MANIFEST_URL_ROOT + manifest_uri)
        else:
            return
    manifest = unzipping_renaming()
    write_tables(manifest)


def check_dirs():
    """
    Simply checks to see if directories exist, makes
    them if they don't
    """
    try:
        if not os.path.isdir(DATA_DIR):
            print("Creating data directory")
            os.makedirs(MANIFEST_DIR)
        if not os.path.isdir(MANIFEST_DIR):
            print("Creating manifest directory")
            os.makedirs(MANIFEST_DIR)
        if not os.path.isdir(JSON_DIR):
            print("Creating JSON directory")
            os.makedirs(JSON_DIR)
    except OSError:
        print("Can't create directories!")
        sys.exit()


def check_manifest_url(uri):
    try:
        with open(MANIFEST_CHECK_FILE, 'r+') as f:
            check_url = f.read()

            if uri == check_url:
                return False

            f.seek(0)
            f.write(uri)

    except FileNotFoundError:
        print("Creating manifest url check-file")
        with open(MANIFEST_CHECK_FILE, 'w') as f:
            f.write(uri)

    return True


def get_manifest_url():
    """
    This function requests an URL for the manifest SQL data
    """
    r = requests.get("https://www.bungie.net/Platform/Destiny2/Manifest/",
                     headers=HEADERS).json()

    if r["ErrorStatus"] == "SystemDisabled":
        print("API is down!")
        sys.exit()

    return r["Response"]["mobileWorldContentPaths"]["en"]


def get_manifest(manifest_url):
    """
    Requests the manifest URL and downloads the zipfile
    database response, prints a nice little progress bar
    showing download progress
    """
    cols, _ = shutil.get_terminal_size()
    cols = cols - 36  # Make space for the file size
    bar_now = cols * '-'
    progress_bar = f"[{bar_now}]"

    r = requests.get(manifest_url, headers=HEADERS, stream=True)
    file_size = int(r.headers["Content-length"]) // 1024

    with open(ZIP_FILE, "wb") as f:
        chunk_cnt = 0
        chunk_size = 1024*1024
        dl_str = "Downloading...    "
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            downloaded = (chunk_cnt * chunk_size) // 1024
            print(f"\r{dl_str}{downloaded}KB/{file_size}KB {progress_bar}", end="")
            sys.stdout.flush()
            # Progress bar re-construction
            progress_pct = (downloaded / file_size)
            bar_now = round(progress_pct * cols)
            bar = bar_now * '#'
            remaining = (cols - bar_now) * '-'
            progress_bar = f"[{bar}{remaining}]"
            chunk_cnt += 1
            sleep(0.5)
        else:
            bar = cols * '#'
            progress_bar = f"[{bar}]"
            print(f"\r{dl_str}{file_size}KB/{file_size}KB {progress_bar}")


def unzipping_renaming():
    """
    Unzips the downloaded zipfile and extracts
    the SQL database, returns the database
    object
    """
    with zipfile.ZipFile(ZIP_FILE, "r") as f:
        manifest = f.namelist()[0]
        f.extractall(MANIFEST_DIR)

    os.remove(ZIP_FILE)

    return MANIFEST_DIR + "/" + manifest


def write_tables(sql):
    """
    Opens the SQL database, gets the table
    names and uses them to query all the tables
    within, converts them to JSON and writes
    them all to individual files
    """
    conn = sqlite3.connect(sql)

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cur.fetchall()
        table_names = [table[0] for table in table_names]

        for entry in table_names:
            try:
                cur.execute('SELECT id,json FROM {}'.format(entry))
                tables = cur.fetchall()
                data = ((str(table[0]), json.loads(table[1])) for table in tables)
                table_dict = {element[0]: element[1] for element in data}

                with open(JSON_DIR + "/" + entry + ".json", "w") as f:
                    json.dump(table_dict, f, indent=4)

                print("- WRITING >> " + entry + ".json")

            except sqlite3.OperationalError:
                print("-- EXCEPTION: SKIPPING " + entry + ".json")
                continue
        else:
            os.remove(sql)
            print("Finished \u263A")


if __name__ == "__main__":
    main()

