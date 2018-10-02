from time import sleep
import requests
import json
import zipfile
import sys
import os


HEADERS = {"X-API-Key": os.environ["BUNGIE_API"]}


def main():
    if check_dirs():
        manifest_url = get_manifest_url()

        get_manifest(manifest_url)

        unzipping_renaming()


def check_dirs():
    if not os.path.isdir("Destiny_Manifest"):
        os.makedirs("Destiny_Manifest")

    return True


def get_manifest_url():
    r = requests.get("https://www.bungie.net/Platform/Destiny2/Manifest/",
                     headers=HEADERS).json()

    manifest_uri = r["Response"]["mobileWorldContentPaths"]["en"]

    manifest_url = "https://www.bungie.net" + manifest_uri

    return manifest_url


def get_manifest(manifest_url):
    r = requests.get(manifest_url, headers=HEADERS, stream=True)
    file_size = int(r.headers["Content-length"]) // 1024000

    chunk_cnt = 0
    CHUNK_SIZE = 1024*1024

    with open("Destiny2Manifest.zip", "wb") as f:
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)
            print(str((chunk_cnt * CHUNK_SIZE) // 1024000)
                  + "MB out of "
                  + str(file_size)
                  + "MB\r", end="")
            sys.stdout.flush()
            chunk_cnt += 1
            sleep(0.5)
        else:
            print(str(file_size)
                  + "MB out of "
                  + str(file_size)
                  + "MB")


def unzipping_renaming():
    file_ = "Destiny2Manifest.zip"
    sql_db = "sql_manifest.content"

    with zipfile.ZipFile(file_, "r") as f:
        f.extractall("Destiny_Manifest")

    os.remove(file_)

    files = os.listdir("Destiny_Manifest")

    manifest = [file_ for file_ in files if file_.endswith(".content")][0]

    os.chdir("Destiny_Manifest")
    os.rename(manifest, sql_db)


if __name__ == "__main__":
    main()

