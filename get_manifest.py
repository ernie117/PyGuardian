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
SQL_DB = "sql_manifest.content"
WORKING_DIR = str(Path.home()) + "/python/" + "destiny/"


def main():

    if check_dirs():
        manifest_url = get_manifest_url()

        get_manifest(manifest_url)

        unzipping_renaming()

        write_tables(SQL_DB)



def check_dirs():

    if not os.path.isdir(MANIFEST_DIR):
        print("Creating tmp manifest directory")
        os.makedirs(MANIFEST_DIR)
    if not os.path.isdir(JSON_DIR):
        print("Creating JSON directory")
        os.makedirs(JSON_DIR)

    return True


def get_manifest_url():

    r = requests.get("https://www.bungie.net/Platform/Destiny2/Manifest/",
                     headers=HEADERS).json()

    manifest_uri = r["Response"]["mobileWorldContentPaths"]["en"]

    manifest_url = f"https://www.bungie.net{manifest_uri}"

    return manifest_url


def get_manifest(manifest_url):

    r = requests.get(manifest_url, headers=HEADERS, stream=True)
    file_size = int(r.headers["Content-length"])

    chunk_cnt = 0
    CHUNK_SIZE = 1024*1024
    cols, rows = shutil.get_terminal_size()
    cols = cols - 24  # Make space for the file size
    bar_now = cols * '-'
    progress_bar = f"[{bar_now}]"

    # TODO finish implementing a download progress bar
    with open("Destiny2Manifest.zip", "wb") as f:
        print("Downloading...")
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)
            downloaded = chunk_cnt * CHUNK_SIZE
            print("\r"
                  + progress_bar
                  + " " + str(downloaded)
                  + "B / "
                  + str(file_size)
                  + "B ",
                  end="")
            sys.stdout.flush()
            progress_pct = (downloaded / file_size)
            bar_now = round(progress_pct * cols)
            printable_bar = bar_now * '#'
            empty = (cols - bar_now) * '-'
            progress_bar = f"[{printable_bar}{empty}]"
            chunk_cnt += 1
            sleep(0.5)
        else:
            print("\r"
                  + progress_bar
                  + " " + str(file_size)
                  + "B / "
                  + str(file_size)
                  + "B ")


def unzipping_renaming():

    with zipfile.ZipFile(ZIP_FILE, "r") as f:
        f.extractall(MANIFEST_DIR)

    os.remove(ZIP_FILE)

    files = os.listdir(MANIFEST_DIR)

    manifest = [file_ for file_ in files if file_.endswith(".content")][0]

    os.chdir(MANIFEST_DIR)
    os.rename(manifest, SQL_DB)


def write_tables(sql):

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

                print("- WRITING >> " + entry)

            except sqlite3.OperationalError:
                print("-- EXCEPTION: SKIPPING " + entry)
                continue
        else:
            os.chdir(WORKING_DIR)
            print("Deleting tmp manifest directory")
            shutil.rmtree(MANIFEST_DIR)
            print("Finished \u263A")


if __name__ == "__main__":
    main()

