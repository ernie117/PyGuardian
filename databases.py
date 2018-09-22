from time import sleep
import requests
import json
import zipfile
import sys
import os


HEADERS = {"X-API-Key": os.environ["BUNGIE_API"]}
r = requests.get("https://www.bungie.net/Platform/Destiny2/Manifest/",
                 headers=HEADERS).json()

manifest_uri = r["Response"]["mobileWorldContentPaths"]["en"]

manifest_url = "https://www.bungie.net" + manifest_uri

r = requests.get(manifest_url, headers=HEADERS, stream=True)
file_size = int(r.headers["Content-length"]) // 1024000

chunk_cnt = 0
CHUNK_SIZE = 1024*1024

with open("Destiny2ManifestZip.zip", "wb") as f:
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

with zipfile.ZipFile("Destiny2ManifestZip.zip", "r") as f:
    f.extractall("Destiny_Manifest")
    archive_name = f.namelist()[0]


