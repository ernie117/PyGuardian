import os
import sqlite3
import json


MANIFEST_DIR = "Destiny_Manifest"
JSON_DIR = "DDB-Files"


def main():

    if check_dirs():
        sql = MANIFEST_DIR + "/" + os.listdir("Destiny_Manifest")[0]

        table_names = get_tables(sql)

        write_tables(table_names, sql)


def check_dirs():

    if not os.path.isdir(MANIFEST_DIR):
        os.makedirs("Destiny_Manifest")
    if not os.path.isdir(JSON_DIR):
        os.makedirs("DDB-Files")

    return True


def get_tables(sql):

    conn = sqlite3.connect(sql)

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cur.fetchall()
        table_names = [table[0] for table in table_names]

    return table_names


def write_tables(table_names, sql):

    conn = sqlite3.connect(sql)

    with conn:
        cur = conn.cursor()
        for entry in table_names:
            try:
                cur.execute('SELECT id,json FROM {}'.format(entry))

                tables = cur.fetchall()

                data = ((str(table[0]), json.loads(table[1])) for table in tables)

                table_dict = {element[0]: element[1] for element in data}

                with open(JSON_DIR + "/" + entry + ".json", "w") as f:
                    json.dump(table_dict, f, indent=4)

                print(entry + " JSON file written...")

            except sqlite3.OperationalError:
                print("-- EXCEPTION: SKIPPING " + entry)
                continue


if __name__ == "__main__":
    main()

