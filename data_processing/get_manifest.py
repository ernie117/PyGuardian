from time import sleep
from ..utils import constants
import requests
import shutil
import sqlite3
import json
import zipfile
import sys
import os


def main(url_check=False):

    check_dirs()
    manifest_uri = get_manifest_url()

    if url_check:
        manifest_uri = check_manifest_url(manifest_uri)
        if manifest_uri is None:
            return

    get_manifest(constants.MANIFEST_URL_ROOT + manifest_uri)
    manifest = unzipping_renaming()
    write_tables(manifest)


def check_dirs():
    """
    Simply checks to see if directories exist, makes
    them if they don't
    """
    try:
        if not os.path.isdir(constants.DATA_DIR):
            print("Creating data directory")
            os.makedirs(constants.MANIFEST_DIR)
        if not os.path.isdir(constants.MANIFEST_DIR):
            print("Creating manifest directory")
            os.makedirs(constants.MANIFEST_DIR)
        if not os.path.isdir(constants.JSON_DIR):
            print("Creating JSON directory")
            os.makedirs(constants.JSON_DIR)
    except OSError:
        print("Can't create directories!")
        sys.exit()


def check_manifest_url(uri):
    try:
        with open(constants.MANIFEST_CHECK_FILE, 'r+') as f:
            check_url = f.read().strip()

            if uri == check_url:
                print("Manifest up-to-date \u2713")
                return

            f.seek(0)
            f.write(uri)

    except FileNotFoundError:
        print("Creating manifest url check-file")
        with open(constants.MANIFEST_CHECK_FILE, 'w') as f:
            f.write(uri)

    return uri


def get_manifest_url():
    """
    Requests an URL for the manifest SQL data
    """
    r = requests.get("https://www.bungie.net/Platform/Destiny2/Manifest/",
                     headers=constants.HEADERS).json()

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

    r = requests.get(manifest_url, headers=constants.HEADERS, stream=True)
    file_size = int(r.headers["Content-length"]) // 1024

    with open(constants.ZIP_FILE, "wb") as f:
        chunk_cnt = 0
        chunk_size = 1024*1024
        dl_str = "Downloading...    "
        bar_char = "\u2588"
        bar_remaining_char = ' '
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            downloaded = (chunk_cnt * chunk_size) // 1024
            print(f"\r{dl_str}{downloaded}KB/{file_size}KB {progress_bar}", end="")
            sys.stdout.flush()
            # Progress bar re-construction
            progress_pct = (downloaded / file_size)
            bar_now = round(progress_pct * cols)
            bar = f"{bar_now * bar_char}"
            remaining = f"{(cols - bar_now) * bar_remaining_char}"
            progress_bar = f"[{bar}{remaining}]"
            chunk_cnt += 1
            sleep(0.5)
        else:
            bar = f"{cols * bar_char}"
            progress_bar = f"[{bar}]"
            print(f"\r{dl_str}{file_size}KB/{file_size}KB {progress_bar}")


def unzipping_renaming():
    """
    Unzips the downloaded zipfile and extracts the SQL
    database, returns the database object
    """
    with zipfile.ZipFile(constants.ZIP_FILE, "r") as f:
        manifest = f.namelist()[0]
        print("Unzipping manifest...")
        f.extractall(constants.MANIFEST_DIR)

    print("Deleting zipfile...")
    os.remove(constants.ZIP_FILE)
    # TODO find most recent sql to write from

    return constants.MANIFEST_DIR + "/" + manifest


def write_tables(sql):
    """
    Opens the SQL database, gets the table names and
    uses them to query all the tables within, converts
    them to JSON and writes them all to individual files
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

                with open(constants.JSON_DIR + "/" + entry + ".json", "w") as f:
                    json.dump(table_dict, f, indent=4)

                print("- WRITING >> " + entry + ".json")

            except sqlite3.OperationalError:
                # Slightly different SQL schema for this one table :/
                cur.execute('SELECT key,json FROM {}'.format(entry))
                tables = cur.fetchall()
                data = ((table[0], json.loads(table[1])) for table in tables)
                table_dict = {element[0]: element[1] for element in data}

                with open(constants.JSON_DIR + "/" + entry + ".json", "w") as f:
                    json.dump(table_dict, f, indent=4)

                print("- WRITING >> " + entry + ".json")

                continue
        else:
            print("Finished \u263A")


if __name__ == "__main__":
    main()

