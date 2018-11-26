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
MANIFEST_DIR = "TMP_Destiny_Manifest"
JSON_DIR = "DDB-Files"
ZIP_FILE = "Destiny2Manifest.zip"
WORKING_DIR = str(Path.home()) + "/python/" + "destiny/"


def main():

    if check_dirs():
        manifest_url = get_manifest_url()
        get_manifest(manifest_url)
        manifest = unzipping_renaming()
        write_tables(manifest)


def check_dirs():
    '''
    Simply checks to see if directories
    for working with/storing data exist,
    creates them if they don't, returns
    True once directories exist
    '''
    try:
        if not os.path.isdir(MANIFEST_DIR):
            print("Creating tmp manifest directory")
            os.makedirs(MANIFEST_DIR)
        if not os.path.isdir(JSON_DIR):
            print("Creating JSON directory")
            os.makedirs(JSON_DIR)
    except OSError:
        print("Can't create directories!")
        return False

    return True


def get_manifest_url():
    '''
    This function requests data from the API
    that contains the part of the url required to
    request the manifest data. It parses out the
    URI then builds the url from it and returns it
    '''
    r = requests.get("https://www.bungie.net/Platform/Destiny2/Manifest/",
                     headers=HEADERS).json()

    if r["ErrorStatus"] == "SystemDisabled":
        print("API is down!")
        sys.exit()

    manifest_uri = r["Response"]["mobileWorldContentPaths"]["en"]
    manifest_url = f"https://www.bungie.net{manifest_uri}"

    return manifest_url


def get_manifest(manifest_url):
    '''
    Requests the manifest URL and downloads the zipfile
    database response, prints a nice little
    progress bar showing download progress
    '''
    # Getting terminal size for progress bar construction
    cols, _ = shutil.get_terminal_size()
    cols = cols - 24  # Make space for the file size
    bar_now = cols * '-'
    progress_bar = f"[{bar_now}]"

    r = requests.get(manifest_url, headers=HEADERS, stream=True)
    file_size = int(r.headers["Content-length"])

    with open("Destiny2Manifest.zip", "wb") as f:
        print("Downloading...")
        chunk_cnt = 1
        CHUNK_SIZE = 1024*1024
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)
            downloaded = chunk_cnt * CHUNK_SIZE
            print(f"\r{progress_bar} {downloaded}B / {file_size}B ", end="")
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
            print(f"\r{progress_bar} {file_size}B / {file_size}B ")


def unzipping_renaming():
    '''
    Unzips the downloaded zipfile and extracts
    the SQL database, returns the database
    object
    '''
    with zipfile.ZipFile(ZIP_FILE, "r") as f:
        manifest = f.namelist()[0]
        f.extractall(MANIFEST_DIR)

    os.remove(ZIP_FILE)
    os.chdir(MANIFEST_DIR)

    return manifest


def write_tables(sql):
    '''
    Opens the SQL database, gets the table
    names and uses them to query all the tables
    within, converts them to JSON and writes
    them all to individual files, deletes
    the temporary manifest directory once
    finished
    '''
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

                os.chdir(WORKING_DIR)
                with open(JSON_DIR + "/" + entry + ".json", "w") as f:
                    json.dump(table_dict, f, indent=4)

                os.chdir(MANIFEST_DIR)
                print("- WRITING >> " + entry + ".json")

            except sqlite3.OperationalError:
                print("-- EXCEPTION: SKIPPING " + entry + ".json")
                continue
        else:
            os.chdir(WORKING_DIR)
            print("Deleting tmp manifest directory")
            shutil.rmtree(MANIFEST_DIR)
            print("Finished \u263A")


if __name__ == "__main__":
    main()

