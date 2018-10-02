import os
import sqlite3
import json


#TODO refactor
def main():
    pass


def check_dirs():
    pass


def get_tables():
    pass


def write_tables():
    pass


MANIFEST_DIR = "Destiny_Manifest/"
JSON_DIR = "DDB-Files/"
SQL = MANIFEST_DIR + os.listdir("Destiny_Manifest")[0]

conn = sqlite3.connect(SQL)

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

            with open(JSON_DIR + entry + ".json", "w") as f:
                json.dump(table_dict, f, indent=4)

            print(entry + " JSON file written...")

        except sqlite3.OperationalError:
            print("-- EXCEPTION: SKIPPING " + entry)
            continue
